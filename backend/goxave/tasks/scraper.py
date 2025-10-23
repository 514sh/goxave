from typing import Callable, Literal

from goxave.api.adapters.scrapers.abc import AbstractScraper
from goxave.api.domain import commands, events, model
from goxave.api.service_layer import message_bus
from goxave.config import PROXY_URL, uow
from goxave.tasks.queue import queue


@queue.task(bind=True, max_retries=3, default_retry_delay=10)
def do_scrape_web(
    self,
    url: str,
    user_id: str,
    user_name: str,
    discord_webhook: str,
    user_email: str,
    handle_scrapers: Callable[
        [str], AbstractScraper | None
    ] = message_bus.handle_scrapers,
) -> Literal[True] | None:
    generated_product = None
    scraper_obj = handle_scrapers(url)
    if not scraper_obj:
        generated_product = None
    else:
        scraper_obj.start(PROXY_URL)
        generated_product = scraper_obj.generated_product()

    if generated_product is None:
        if self.request.retries >= self.max_retries:
            error_notified = events.NotifyErrorAddingNewItem(
                discord_webhook=discord_webhook,
                user_name=user_name,
                user_email=user_email,
                product_url=url,
            )
            message_bus.handle(error_notified, uow)
        self.retry(
            countdown=10,
            exc=Exception(
                f"Result was None, retrying {self.request.retries}/{self.max_retries}..."
            ),
        )
    else:
        product_image_model = model.ProductImage(
            src=generated_product["product_image"]["src"],
            alt=generated_product["product_image"]["alt"],
        )
        product_model = model.Product(
            url=generated_product["url"],
            product_name=generated_product["product_name"],
            product_price=generated_product["product_price"],
            product_image=product_image_model,
            price_history=None,
            user_ids=[user_id],
        )
        user_model = model.User(
            id=user_id,
            my_products=[product_model.url_id],
        )

        handle_add_new_item = commands.AddNewItem(
            product=product_model, user=user_model
        )
        message_bus.handle(handle_add_new_item, uow)
    return True


@queue.task(bind=True)
def test_print(self):
    print("testing schedule...")
    return "testing... print"


@queue.task(bind=True)
def scheduled_scrape(
    self,
    handle_scrapers: Callable[
        [str], AbstractScraper | None
    ] = message_bus.handle_scrapers,
):
    print("scraping schedule start.....")
    with uow:
        for saved_product in uow.products.iterator():
            latest_price = None
            scraper_obj = handle_scrapers(saved_product.url)
            if scraper_obj:
                scraper_obj.start(PROXY_URL)
                latest_price = scraper_obj.product_price
            if latest_price is None:
                latest_price = saved_product.product_price
            if isinstance(saved_product, model.Product):
                my_trackers = [
                    tracker for tracker in uow.users.all(saved_product.my_trackers)
                ]
                saved_product.add_price_history(
                    product_price=latest_price, my_trackers=my_trackers
                )
            handle_update_product_price = commands.UpdateProductPrice(
                product=saved_product
            )
            message_bus.handle(handle_update_product_price, uow)
        uow.commit()
    return "scraped done"

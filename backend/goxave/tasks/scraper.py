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
    handle_scrapers: Callable[
        [str], AbstractScraper | None
    ] = message_bus.handle_scrapers,
) -> Literal[True] | None:
    print(f"scraper webhook: {discord_webhook}")
    generated_product = None
    scraper_obj = handle_scrapers(url)
    if not scraper_obj:
        generated_product = None
    else:
        scraper_obj.start(PROXY_URL)
        generated_product = scraper_obj.generated_product()

    if generated_product is None:
        if self.request.retries >= self.max_retries:
            print("Max retries exceeded")
            error_notified = events.NotifyErrorAddingNewItem(
                discord_webhook=discord_webhook,
                user_name=user_name,
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
        print("scraping...")
        product_image_model = model.ProductImage(
            src=generated_product["product_image"]["src"],
            alt=generated_product["product_image"]["alt"],
        )
        print(f"product_image mode: {product_image_model}")
        product_model = model.Product(
            url=generated_product["url"],
            product_name=generated_product["product_name"],
            product_price=generated_product["product_price"],
            product_image=product_image_model,
            price_history=None,
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

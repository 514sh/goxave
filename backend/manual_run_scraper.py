import inspect
import os

from goxave.api.service_layer.message_bus import handle_scrapers
from goxave.config import PROXY_URL


def main():
    url = os.environ["URL"]
    store_scraper = handle_scrapers(url=url)
    if not store_scraper:
        return None

    store_scraper.start(proxy_server=PROXY_URL, screenshot=True)
    for name, value in inspect.getmembers(
        type(store_scraper), lambda v: isinstance(v, property)
    ):
        print(f"{name} = {getattr(store_scraper, name)}")


if __name__ == "__main__":
    main()

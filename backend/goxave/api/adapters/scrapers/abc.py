import abc

from goxave.api.adapters.browser_automation.playwright import SyncPlaywright
from goxave.api.adapters.parsers.html.bs4 import HTMLParser


class AbstractScraper(abc.ABC):
    def __init__(self, url: str, bypassed: bool = False, timeout: int = 200_000):
        self._url = url
        self._bypassed = bypassed
        self._timeout = timeout

    def parser(self, html_content) -> HTMLParser:
        return HTMLParser(html_content)

    def web_automator(self) -> SyncPlaywright:
        return SyncPlaywright()

    @abc.abstractmethod
    def start(self, proxy_server: str, screenshot: bool = False):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def url(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def product_price(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def product_name(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def product_image(self):
        raise NotImplementedError

    def generated_product(self) -> dict | None:
        if not self.product_price and not self.product_name:
            return None
        return {
            "url": self.url,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "product_image": self.product_image,
            "price_history": None,
        }

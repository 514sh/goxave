from goxave.api.adapters.scrapers.abc import AbstractScraper


class LazadaScraper(AbstractScraper):
    def __init__(self, url: str):
        self.__url = url
        self.__product_price: str | None = None
        self.__product_name: str | None = None

    def start(self) -> None:
        pass

    @property
    def url(self) -> str:
        return self.__url

    @property
    def product_price(self) -> str | None:
        return self.__product_price

    @property
    def product_name(self) -> str | None:
        return self.__product_name

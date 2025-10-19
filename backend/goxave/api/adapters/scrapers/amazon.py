from bs4 import Tag
from goxave.api.adapters.scrapers.abc import AbstractScraper


class AmazonStooreScraper(AbstractScraper):
    def __init__(self, url: str):
        self.__url = url
        self.__product_price: Tag | None = None
        self.__product_name: Tag | None = None

    def start(self, proxy_server: str, screenshot: bool = False) -> None:
        html_content = ""
        with self.web_automator() as p:
            if proxy_server:
                browser = p.chromium.launch(proxy={"server": proxy_server})
            else:
                browser = p.chromium.launch()
            page = browser.new_page()
            wait_until = "load"
            page.goto(self.__url, wait_until=wait_until, timeout=600000)
            if screenshot:
                page.screenshot(path="TEST_DATA/amazon_test.png")
            html_content = page.content()
            browser.close()

        html_parser = self.parser(html_content=html_content)
        print("done")
        root = html_parser.find_all(id="ppd")
        current_price = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("centerCol", "id", None),
                ("apex_desktop", "id", None),
                ("corePriceDisplay_desktop_feature_div", "id", None),
                ("aok-offscreen", "class", None),
            ],
        )
        current_name = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("centerCol", "id", None),
                ("productTitle", "id", "span"),
            ],
        )

        current_product_image = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("leftCol", "id", None),
                ("imageBlock", "id", None),
                ("imgTagWrapper", "class", None),
                ("a-dynamic-image", "class", "img"),
            ],
        )

        self.__product_price = html_parser.get_item_given_index(current_price, 0)
        self.__product_name = html_parser.get_item_given_index(current_name, 0)
        self.__product_image = html_parser.get_item_given_index(
            current_product_image, 0
        )

    @property
    def url(self) -> str:
        if isinstance(self.__url, str):
            self.__url = self.__url.strip()
        return self.__url

    @property
    def product_price(self) -> str | None:
        if not self.__product_price:
            return None
        if isinstance(self.__product_price.string, str):
            return self.__product_price.string.strip()
        return self.__product_price.string

    @property
    def product_name(self) -> str | None:
        if not self.__product_name:
            return None
        if isinstance(self.__product_name.string, str):
            return self.__product_name.string.strip()
        return self.__product_name.string

    @property
    def product_image(self):
        if not self.__product_image:
            return None
        alt = self.__product_image.get("alt")
        src = self.__product_image.get("src")
        if isinstance(alt, str):
            alt = alt.strip()
        if isinstance(src, str):
            src = src.strip()
        return {"alt": alt, "src": src}

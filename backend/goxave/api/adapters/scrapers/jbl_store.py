from bs4 import Tag

from goxave.api.adapters.scrapers.abc import AbstractScraper


class JBLStoreScraper(AbstractScraper):
    def __init__(self, url: str):
        self.__url = url
        self.__product_price: Tag | None = None
        self.__product_name: Tag | None = None

    def start(self, proxy_server: str) -> None:
        html_content = ""
        with self.web_automator() as p:
            if proxy_server:
                browser = p.chromium.launch(proxy={"server": proxy_server})
            else:
                browser = p.chromium.launch()
            page = browser.new_page()
            wait_until = "load"
            page.goto(self.__url, wait_until=wait_until, timeout=600000)

            page.screenshot(path="TEST_DATA/test.png")
            html_content = page.content()
            browser.close()

        html_parser = self.parser(html_content=html_content)

        root = html_parser.find_all(id="shopify-section-template--15588994023518__main")

        current_price = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("modal_price", "class", None),
                ("current_price", "class", None),
                ("money", "class", None),
            ],
        )
        current_name = html_parser.nested_find_all(
            root,  # type: ignore
            params=[("product_name", "class", None), (None, None, "a")],
        )

        current_product_image = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("flickity-slider", "class", None),
                (["product-gallery__image", "is-selected"], "class", None),
                ("image__container", "class", None),
                ("zoom-container", "class", "span"),
                ("zoomImg", "class", "img"),
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

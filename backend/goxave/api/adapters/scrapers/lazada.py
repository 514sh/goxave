from goxave.api.adapters.scrapers.abc import AbstractScraper


class LazadaScraper(AbstractScraper):
    def __init__(self, url: str, bypassed=True):
        super().__init__(url=url, bypassed=bypassed)

    def start(self, proxy_server: str, screenshot: bool = False) -> None:
        html_content = ""
        with self.web_automator() as p:
            if proxy_server and not self._bypassed:
                browser = p.chromium.launch(proxy={"server": proxy_server})
            else:
                browser = p.chromium.launch()
            page = browser.new_page()
            try:
                print("Attempting navigation with wait_until='networkidle'...")
                page.goto(self.url, wait_until="networkidle", timeout=self._timeout)
                final_url = page.url
                print(f"Success with networkidle. Final URL: {final_url}")
            except TimeoutError as e:
                # Fallback to load if networkidle times out
                print(
                    f"Networkidle timed out: {str(e)}. Falling back to wait_until='load'..."
                )
                page.goto(self.url, wait_until="load", timeout=self._timeout)
                final_url = page.url
                print(f"Success with load. Final URL: {final_url}")
            except Exception as e:
                # Handle other potential errors
                print(f"An unexpected error occurred: {str(e)}")
            finally:
                # Optionally, interact with the page
                if screenshot:
                    page.screenshot(path="TEST_DATA/amazon_test.png")
                html_content = page.content()
                browser.close()

        html_parser = self.parser(html_content=html_content)
        root = html_parser.find_all(id="root")
        currency = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("pdp-v2-product-price-content-salePrice", "class", None),
                ("pdp-v2-product-price-content-salePrice-sign", "class", None),
            ],
        )
        price = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("pdp-v2-product-price-content-salePrice", "class", None),
                ("pdp-v2-product-price-content-salePrice-amount", "class", None),
            ],
        )

        current_name = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("pdp-product-title", "class", None),
                ("pdp-mod-product-badge-title-v2", "class", None),
            ],
        )

        current_product_image = html_parser.nested_find_all(
            root,  # type: ignore
            params=[
                ("module_item_gallery_1", "id", None),
                ("gallery-preview-panel-v2__content", "class", None),
                (
                    ["pdp-mod-common-image", "gallery-preview-panel-v2__image"],
                    "class",
                    None,
                ),
            ],
        )
        self.__currency = html_parser.get_item_given_index(currency, 0)
        self.__price = html_parser.get_item_given_index(price, 0)
        self.__product_name = html_parser.get_item_given_index(current_name, 0)
        self.__product_image = html_parser.get_item_given_index(
            current_product_image, 0
        )

    @property
    def url(self) -> str:
        if isinstance(self._url, str):
            self._url = self._url.strip()
        return self._url

    @property
    def product_price(self) -> str | None:
        if not self.__currency or not self.__price:
            return None
        current_price = []
        for price_info in [self.__currency, self.__price]:
            price = ""
            if isinstance(price_info.string, str):
                price = price_info.string.strip()
            else:
                price = price_info.string
            current_price.append(price)
        return "".join(current_price)

    @property
    def product_name(self) -> str | None:
        product_name = None
        if not self.__product_name:
            return product_name
        if isinstance(self.__product_name.string, str):
            product_name = self.__product_name.string.strip()
        if not product_name:
            product_name = self.__product_name.get_text(strip=True)
        return product_name

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

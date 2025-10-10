import re
from dataclasses import dataclass

from goxave.api.domain import events
from goxave.api.domain.utilities import dns_id, get_currency_symbol, unix_millis, url_id

type ProductIdentifier = str

type UserIdentifier = str


@dataclass
class Price:
    price: float
    currency: str | None = None
    timestamp: int = unix_millis()


@dataclass(frozen=True)
class Login:
    session_id: str
    token: str = ""
    isLoggedOut: bool = False


@dataclass
class ProductImage:
    src: str = ""
    alt: str = ""


class Product:
    def __init__(
        self,
        price_history: list[Price] | None = None,
        url: str = "",
        product_name: str = "",
        product_price: str = "",
        id: str = "",
        product_image: ProductImage = ProductImage(),
        user_ids: list[UserIdentifier] | None = None,
    ):
        self.__events = []
        self.__url = url
        self.__product_name = product_name
        self.__product_price = product_price
        self.__price_history = price_history if price_history else []
        self.__id = id or url_id(self.__url)
        self.__product_image = product_image
        self.__user_ids = user_ids if user_ids else []
        if not price_history:
            self.add_price_history(product_price=product_price)

    @property
    def url(self) -> str:
        return self.__url

    @property
    def url_id(self) -> str:
        return self.__id

    @property
    def product_name(self):
        return self.__product_name

    @property
    def product_price(self):
        return self.__product_price

    @property
    def price_history(self) -> list[Price]:
        return [*self.__price_history]

    @property
    def product_image(self) -> ProductImage:
        return self.__product_image

    @property
    def my_trackers(self) -> list[str]:
        return [*self.__user_ids]

    @property
    def events(self):
        return [*self.__events]

    def add_event(self, event):
        self.__events.append(event)

    def add_price_history(
        self,
        product_price: str,
        timestamp: int | None = None,
        my_trackers: list | None = None,
    ) -> None:
        if not product_price:
            return None
        price_decimal = self.__get_price_in_decimal(product_price)
        currency = self.__get_currency(product_price)
        if timestamp:
            price = Price(price=price_decimal, currency=currency, timestamp=timestamp)
        else:
            price = Price(
                price=price_decimal, currency=currency, timestamp=unix_millis()
            )
        self.__price_history.append(price)
        if len(self.__price_history) >= 2:
            latest_history = self.__price_history[-1]
            second_latest_history = self.__price_history[-2]
            if second_latest_history.price != latest_history.price:
                self.__events.append(
                    events.NotifyUserOnPriceChange(
                        product_url=self.url,
                        my_trackers=my_trackers or [],
                        previous_price=f"{second_latest_history.currency} {second_latest_history.price}",
                        current_price=f"{latest_history.currency} {latest_history.price}",
                    )
                )

    def __get_price_in_decimal(self, value: str) -> float:
        if not isinstance(value, str):
            return float(0)
        price_str = "".join(re.findall(r"[0-9.]", value))
        return round(float(price_str), 2)

    def __get_currency(self, value: str) -> None | str:
        if not isinstance(value, str):
            self.__events.append(
                events.NotifyAdminRegardingProduct(
                    message=f"Product: {self.url} currency: {value} gives non string currency."
                )
            )
            return None
        currency_str = "".join(re.findall(r"[^0-9,.\_\-\s]", value))
        currency_symbol = get_currency_symbol(currency_str)
        if not currency_symbol:
            self.__events.append(
                events.NotifyAdminRegardingProduct(
                    message=f"Product: {self.url} currency: {value} is not in the currency symbols/codes set."
                )
            )
            return None
        return currency_symbol


class User:
    def __init__(
        self,
        name: str = "",
        email: str = "",
        join_date=None,
        current_session: str | None = None,
        my_products: list[ProductIdentifier] | None = None,
        id: str = "",
        discord_webhook=None,
    ):
        self.__name = name
        self.__email = email
        self.__join_date = join_date or unix_millis()
        self.__current_session = current_session
        self.__my_products = my_products if my_products else []
        self.__id = id or dns_id(email)
        self.__discord_webhook = discord_webhook
        self.__events = []

    @property
    def email(self) -> str:
        return self.__email

    @property
    def dns_id(self) -> str:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def join_date(self) -> None | int:
        return self.__join_date

    @property
    def current_session(self) -> str | None:
        return self.__current_session

    @property
    def my_products(self) -> list[ProductIdentifier]:
        return self.__my_products

    @property
    def discord_webhook(self) -> str | None:
        return self.__discord_webhook

    @property
    def events(self):
        return [*self.__events]

    def notify_new_tracked_item_is_added(self, product: Product):
        if product:
            self.__events.append(
                events.NotifyNewItemAdded(
                    product_url=product.url,
                    user_name=self.__name,
                    discord_webhook=self.__discord_webhook,
                )
            )

import os
from dataclasses import dataclass


class Event:
    pass


@dataclass
class NotifyNewItemAdded(Event):
    product_url: str
    user_name: str
    user_email: str
    discord_webhook: str | None = None


@dataclass
class NotifyErrorAddingNewItem(Event):
    product_url: str
    user_name: str
    discord_webhook: str | None = None


@dataclass
class NotifyNewUserAdded(Event):
    pass


@dataclass
class NotifyAdminRegardingProduct(Event):
    message: str
    admin_discord_webhook: str = os.environ.get("ADMIN_DISCORD_WEBHOOK", "")


@dataclass
class NotifyUserOnPriceChange(Event):
    my_trackers: list
    product_url: str
    previous_price: str
    current_price: str

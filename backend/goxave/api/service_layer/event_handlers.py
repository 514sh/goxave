import httpx

from goxave.api.domain.events import (
    NotifyErrorAddingNewItem,
    NotifyNewItemAdded,
    NotifyUserOnPriceChange,
)


def notify_discord_new_item_added(event: NotifyNewItemAdded, uow):
    discord_webhook = event.discord_webhook
    user_name = event.user_name
    product_url = event.product_url
    data = {
        "content": f"Hello {user_name}! You have new saved product ready to be tracked. {product_url}"
    }
    if discord_webhook:
        response = httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
        return response
    return None


def notify_discord_on_error_adding_new_item(event: NotifyErrorAddingNewItem, uow):
    discord_webhook = event.discord_webhook
    user_name = event.user_name
    product_url = event.product_url
    data = {
        "content": f"Hello {user_name}! We are unable to add the following product to your tracked items at this moment. {product_url}. Please try again!"
    }
    if discord_webhook:
        response = httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
        return response
    return None

    pass


def notify_discord_on_price_change(event: NotifyUserOnPriceChange, uow):
    for user in event.my_trackers:
        discord_webhook = user.discord_webhook
        product_url = event.product_url
        previous_price = event.previous_price
        current_price = event.current_price
        data = {
            "content": f"Hello {user.name}, There's a price change for {product_url}. From {previous_price} to {current_price}. Check it out now!"
        }
        httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
    return None

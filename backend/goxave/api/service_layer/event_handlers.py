import httpx

from goxave.api.domain.events import NotifyErrorAddingNewItem, NotifyNewItemAdded


def notify_discord_new_item_added(event: NotifyNewItemAdded, uow):
    print("notify_discord_new_item_added is called....")
    discord_webhook = event.discord_webhook
    user_name = event.user_name
    product_url = event.product_url
    print(f"notifying....{discord_webhook}")
    data = {
        "content": f"Hello {user_name}! You have new saved product ready to be tracked. {product_url}"
    }
    print(f"my data to sent to discord: {data}")
    if discord_webhook:
        response = httpx.post(
            discord_webhook, headers={"Content-Type": "application/json"}, json=data
        )
        print(f"discord response: {response.text}")
        return response
    return None


def notify_discord_on_error_adding_new_item(event: NotifyErrorAddingNewItem, uow):
    print("notify_discord_new_item_added is called....")
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
        print(f"discord response: {response.text}")
        return response
    return None

    pass

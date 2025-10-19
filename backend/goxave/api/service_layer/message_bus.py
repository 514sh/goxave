from goxave.api.adapters.scrapers import abc, amazon, datablitz, jbl_store, lazada
from goxave.api.domain import commands, events
from goxave.api.service_layer import command_handlers, event_handlers


def handle_scrapers(
    url: str,
) -> abc.AbstractScraper | None:
    if isinstance(url, str):
        url = url.strip()
    stores = {
        "https://jblstore.com.ph/": jbl_store.JBLStoreScraper,
        "https://www.amazon.com/": amazon.AmazonStooreScraper,
        "https://www.lazada.com.ph/": lazada.LazadaScraper,
        "https://ecommerce.datablitz.com.ph/": datablitz.DatablitzStoreScraper,
    }
    for store, scraper in stores.items():
        if url.startswith(store):
            return scraper(url)
    return None


EVENT_HANDLERS = {
    events.NotifyNewItemAdded: [event_handlers.notify_discord_new_item_added],
    events.NotifyErrorAddingNewItem: [
        event_handlers.notify_discord_on_error_adding_new_item
    ],
    events.NotifyUserOnPriceChange: [event_handlers.notify_discord_on_price_change],
}

COMMAND_HANDLERS = {
    commands.AddNewLogin: command_handlers.handle_login,
    commands.AddNewItem: command_handlers.handle_add_new_item,
    commands.GetMyProducts: command_handlers.handle_get_users_item,
    commands.RemovedOneSavedProduct: command_handlers.handle_removed_one_saved_product,
    commands.GetOneSavedProduct: command_handlers.get_one_saved_product,
    commands.UpdateUserInfo: command_handlers.update_user_info,
    commands.FetchUserInfo: command_handlers.fetch_user_info,
    commands.UpdateProductPrice: command_handlers.update_product_price,
}


def handle(message, uow):
    queue = [message]
    results = []
    while queue:
        current_message = queue.pop(0)
        if isinstance(current_message, events.Event):
            handle_events(current_message, uow, queue)
        elif isinstance(current_message, commands.Command):
            results.append(handle_commands(current_message, uow, queue))
    return results


def handle_events(event, uow, queue):
    for handler in EVENT_HANDLERS[type(event)]:
        handler(event, uow)
        for new_event in uow.collect_events():
            queue.append(new_event)


def handle_commands(command, uow, queue):
    handler = COMMAND_HANDLERS[type(command)]
    result = handler(command, uow)
    for new_event in uow.collect_events():
        queue.append(new_event)
    return result

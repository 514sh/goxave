# from goxave.api.domain.events import NotifyNewItemAdded
# from goxave.api.domain.model import Product, User
# from goxave.api.service_layer.event_handlers import notify_discord_new_item_added
# from goxave.api.service_layer.unit_of_work import UnitOfWork


# def test_notify_discord_new_item_added(uow: UnitOfWork, product: Product, user: User):
# event_notify_new_item_added = NotifyNewItemAdded(product=product, user=user)
# test_notify = notify_discord_new_item_added(
# event=event_notify_new_item_added, uow=uow
# )

# assert test_notify is None

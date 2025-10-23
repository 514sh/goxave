from typing import Literal

from goxave.api.domain import commands
from goxave.api.domain.model import User
from goxave.api.service_layer.unit_of_work import UnitOfWork


def handle_login(command: commands.AddNewLogin, uow: UnitOfWork):
    with uow:
        uow.logins.add(command.login)
        user_exists = uow.users.get(command.user)
        if not user_exists:
            uow.users.add(command.user)
        else:
            user_exists = uow.users.update(command.user)
        uow.commit()
    return user_exists or True


def handle_add_new_item(command: commands.AddNewItem, uow: UnitOfWork) -> User | None:
    with uow:
        new_product = uow.products.get(command.product)
        current_user = uow.users.get(command.user)
        print(f"current_user: {current_user}")
        print(f"command user: {command.user}")
        if not new_product:
            uow.products.add(command.product)

        if current_user and command.user.my_products[0] not in current_user.my_products:
            current_user.notify_new_tracked_item_is_added(command.product)
            current_user = uow.users.push(current_user, command.product.url_id)
            print(f"user: {command.user.dns_id}")
            uow.products.push(product=command.product, new_user_id=command.user.dns_id)

        uow.commit()
    return current_user


def handle_get_users_item(
    command: commands.GetMyProducts, uow: UnitOfWork
) -> list | None:
    my_products = None
    with uow:
        current_user = uow.users.get(command.user)
        if not current_user:
            return None
        product_ids = current_user.my_products
        my_products = uow.products.all(product_ids)
        uow.commit()
    return my_products


def handle_removed_one_saved_product(
    command: commands.RemovedOneSavedProduct, uow: UnitOfWork
) -> None | Literal[True]:
    with uow:
        current_user = uow.users.get(command.user)
        if not current_user:
            return None
        is_removed = uow.users.pull(current_user, command.product.url_id)
        uow.products.pull(command.product, command.user.dns_id)
        uow.commit()

    return is_removed


def get_one_saved_product(
    command: commands.GetOneSavedProduct, uow: UnitOfWork
) -> None | dict:
    with uow:
        fetched_product = uow.products.get(command.product)
        uow.commit()

    return fetched_product  # type: ignore


def update_user_info(command: commands.UpdateUserInfo, uow: UnitOfWork) -> User | None:
    with uow:
        updated_user = uow.users.update(command.user)
        uow.commit()
    return updated_user


def fetch_user_info(command: commands.FetchUserInfo, uow: UnitOfWork) -> User | None:
    with uow:
        fetched_user = uow.users.get(command.user)
        uow.commit()
    return fetched_user


def update_product_price(command: commands.UpdateProductPrice, uow: UnitOfWork):
    with uow:
        uow.products.push(product=command.product)
        uow.commit()
    return None

from dataclasses import dataclass

from goxave.api.domain.model import Login, Product, User


class Command:
    pass


@dataclass
class AddNewItem(Command):
    product: Product
    user: User


@dataclass
class AddNewUser(Command):
    pass


@dataclass
class AddNewLogin(Command):
    login: Login
    user: User


@dataclass
class GetMyProducts(Command):
    user: User


@dataclass
class RemovedOneSavedProduct(Command):
    user: User
    product_id: str


@dataclass
class GetOneSavedProduct(Command):
    product: Product


@dataclass
class UpdateUserInfo(Command):
    user: User


@dataclass
class FetchUserInfo(Command):
    user: User


@dataclass
class UpdateProductPrice(Command):
    product: Product

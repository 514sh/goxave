import abc
from dataclasses import asdict
from typing import Iterator, Literal

from pymongo import ReturnDocument
from pymongo.collection import Collection
from pymongo.database import Database

from goxave.api.domain.model import (
    Login,
    Price,
    Product,
    ProductIdentifier,
    ProductImage,
    User,
    UserIdentifier,
)


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, *args, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError


class ProductRepository(AbstractRepository):
    def __init__(self, session, db: Database):
        self._session = session
        self._collection: Collection = db["products"]
        self.seen = set()

    def add(self, product: Product):
        serialized_product = self.__serialize(product)
        self._collection.insert_one(serialized_product, session=self._session)

    def get(
        self,
        product: Product,
    ) -> Product | None:
        found_product = self._collection.find_one(
            {"_id": product.url_id}, session=self._session
        )
        if not found_product:
            return None
        return self.__deserialize(found_product)

    def push(self, product: Product, new_user_id: str | None = None) -> Product | None:
        if not product and not product.price_history:
            return None
        filter_query = {"_id": product.url_id}
        to_update = {}
        latest_price = product.price_history[-1]
        if product.price_history:
            to_update["price_history"] = asdict(latest_price)
        if new_user_id:
            to_update["my_trackers"] = new_user_id
        update_operation = {
            "$push": to_update,
            "$set": {"product_price": f"{latest_price.currency} {latest_price.price}"},
        }
        updated_document = self._collection.find_one_and_update(
            filter_query, update_operation, return_document=ReturnDocument.AFTER
        )
        if updated_document:
            self.seen.add(product)
            return self.__deserialize(updated_document)
        return None

    def pull(self, product: Product, user_id: str) -> None | Literal[True]:
        if not product and user_id:
            return None
        filter_query = {"_id": product.url_id}
        update_operation = {"$pull": {"my_trackers": user_id}}
        update_document = self._collection.update_one(filter_query, update_operation)
        if update_document and update_document.modified_count:
            return True
        return None

    def all(
        self,
        products: list[ProductIdentifier],
    ) -> list[Product] | None:
        my_products = self._collection.find({"_id": {"$in": products}})
        if not my_products:
            return None
        return [self.__deserialize(product) for product in my_products]

    def iterator(
        self,
    ) -> Iterator[Product]:
        with self._collection.find({}) as cursor:
            for product in cursor:
                yield self.__deserialize(product)

    def __serialize(self, product: Product):
        return {
            "_id": product.url_id,
            "url": product.url,
            "product_name": product.product_name,
            "product_price": product.product_price,
            "price_history": [
                {
                    "price": hist.price,
                    "currency": hist.currency,
                    "timestamp": hist.timestamp,
                }
                for hist in product.price_history
            ],
            "product_image": {
                "src": product.product_image.src,
                "alt": product.product_image.alt,
            },
            "my_trackers": product.my_trackers,
        }

    def __deserialize(self, result: dict) -> Product:
        return Product(
            url=result["url"],
            product_name=result["product_name"],
            product_price=result["product_price"],
            price_history=[Price(**hist) for hist in result["price_history"]],
            product_image=ProductImage(**result["product_image"]),
            id=result["_id"],
            user_ids=result["my_trackers"],
        )


class UserRepository(AbstractRepository):
    def __init__(self, session, db: Database):
        self._session = session
        self._collection: Collection = db["users"]
        self.seen = set()

    def add(self, user: User) -> None:
        self._collection.insert_one(self.__serialize(user), session=self._session)
        self.seen.add(user)

    def get(self, user: User) -> User | None:
        found_user = self._collection.find_one(
            {"_id": user.dns_id}, session=self._session
        )
        if not found_user:
            return None
        return self.__deserialize(found_user)

    def all(self, user_ids: list[UserIdentifier]) -> Iterator[User]:
        cursor = self._collection.find({"_id": {"$in": user_ids}})
        for user in cursor:
            yield self.__deserialize(user)

    def update(self, user: User) -> User | None:
        filter_query = {"_id": user.dns_id}
        to_update = {}
        if user.current_session:
            to_update["current_session"] = user.current_session
        if user.discord_webhook:
            to_update["discord_webhook"] = user.discord_webhook
        update_operation = {"$set": to_update}
        updated_document = self._collection.find_one_and_update(
            filter_query, update_operation, return_document=ReturnDocument.AFTER
        )

        if updated_document:
            return self.__deserialize(updated_document)
        return None

    def push(self, user: User, new_product_id: str) -> User | None:
        filter_query = {"_id": user.dns_id}
        update_operation = {"$push": {"my_products": new_product_id}}
        updated_document = self._collection.find_one_and_update(
            filter_query, update_operation, return_document=ReturnDocument.AFTER
        )
        if updated_document:
            self.seen.add(user)
            return self.__deserialize(updated_document)
        return None

    def pull(self, user: User, product_id: str) -> None | Literal[True]:
        if not user and product_id:
            return None
        serialize_user = self.__serialize(user)
        filter_query = {"_id": serialize_user["_id"]}
        update_operation = {"$pull": {"my_products": product_id}}
        update_document = self._collection.update_one(filter_query, update_operation)
        if update_document and update_document.modified_count:
            return True
        return None

    def __serialize(self, user: User):
        return {
            "_id": user.dns_id,
            "email": user.email,
            "name": user.name,
            "join_date": user.join_date,
            "current_session": user.current_session,
            "discord_webhook": user.discord_webhook,
            "my_products": [product for product in user.my_products],
        }

    def __deserialize(self, result: dict):
        return User(
            name=result["name"],
            email=result["email"],
            join_date=result["join_date"],
            current_session=result["current_session"],
            discord_webhook=result["discord_webhook"],
            my_products=[product_id for product_id in result["my_products"]],
        )


class LoginRepository(AbstractRepository):
    def __init__(self, session, db: Database):
        self._session = session
        self._collection: Collection = db["logins"]
        self.seen = set()

    def add(self, login: Login):
        serialized_login = self.__serialize(login)
        self._collection.insert_one(serialized_login, session=self._session)
        self.seen.add(login)

    def get(self, login: Login) -> Login | None:
        found_session = self._collection.find_one(
            {"_id": login.session_id}, session=self._session
        )
        if not found_session:
            return None
        return self.__deserialize(found_session)

    def invalidate(self, login: Login):
        filter_query = {"_id": login.session_id}
        update_operation = {"$set": {"isLoggedOut": True}}
        updated_document = self._collection.find_one_and_update(
            filter_query, update_operation, return_document=ReturnDocument.AFTER
        )
        if updated_document:
            return self.__deserialize(updated_document)
        return None

    def __serialize(self, login: Login):
        return {
            "_id": login.session_id,
            "token": login.token,
            "isLoggedOut": login.isLoggedOut,
        }

    def __deserialize(self, result: dict):
        return Login(
            session_id=result["_id"],
            token=result["token"],
            isLoggedOut=result["isLoggedOut"],
        )

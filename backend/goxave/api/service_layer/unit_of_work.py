from pymongo.client_session import ClientSession

from goxave.api.adapters.repositories.mongodb import (
    LoginRepository,
    ProductRepository,
    UserRepository,
)


class UnitOfWork:
    def __init__(self, client, db_name):
        self._client = client
        self._db_name = db_name

    def __enter__(self):
        self._session: ClientSession = self._client.start_session()
        self._session.start_transaction()
        self.products = ProductRepository(
            session=self._session, db=self._client[self._db_name]
        )
        self.users = UserRepository(
            session=self._session, db=self._client[self._db_name]
        )
        self.logins = LoginRepository(
            session=self._session, db=self._client[self._db_name]
        )
        self.__committed = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            print(f"exc: {exc_type} committed? {self.__committed}")
            if exc_type is not None or not self.__committed:
                self.rollback()
        finally:
            if not self._session.has_ended:
                self._session.end_session()
        return False

    def _commit(self):
        self._session.commit_transaction()

    def rollback(self):
        self.__committed = False
        self._session.abort_transaction()

    def commit(self):
        self.__committed = True
        self._commit()

    def collect_events(self):
        if not all(
            [hasattr(self, "products"), hasattr(self, "users"), hasattr(self, "logins")]
        ):
            yield None
        for repo in [self.users, self.products, self.logins]:
            while repo.seen:
                aggregate = repo.seen.pop()
                for event in getattr(aggregate, "events", []):
                    yield event

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
        self._session: ClientSession | None = None
        self._in_transaction = False

    def __enter__(self):
        self._session = self._client.start_session()
        if self._session is None:
            return self
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
        self._in_transaction = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            if self._in_transaction:
                self.rollback()
            self._session.end_session()
            self._session = None
            self._in_transaction = False

    def commit(self):
        if self._session and self._in_transaction:
            self._session.commit_transaction()
            self._in_transaction = False

    def rollback(self):
        if self._session and self._in_transaction:
            self._session.abort_transaction()
            self._in_transaction = False

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

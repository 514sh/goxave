import os

import pytest
from fastapi.testclient import TestClient

from goxave.api.adapters.repositories.mongodb import (
    LoginRepository,
    ProductRepository,
    UserRepository,
)
from goxave.api.domain.model import Login, Product, User
from goxave.api.service_layer.unit_of_work import UnitOfWork
from goxave.config import create_session, get_database_client
from goxave.run import app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def lazada_url() -> str:
    return "https://www.lazada.com.ph/products/beelink-eq14-mini-pc-intel-lake-n150-up-to-36ghz-ddr4-3200mhz-pcie-30-m2-ssd-windows-11-pro-dual-25g-lan-wifi6-bt52-desktop-for-office-1-year-warranty-i4596802114.html"


@pytest.fixture
def get_client():
    client = get_database_client()
    print("\nstarting database test_goxave...\n")
    yield client
    print("\ndone...deleting database test_goxave\n")
    client.drop_database("test_goxave")


@pytest.fixture
def mongodb_session(get_client):
    session = create_session(get_client)
    yield session
    session.end_session()


@pytest.fixture
def product_repository(mongodb_session, get_client) -> ProductRepository:
    return ProductRepository(mongodb_session, get_client["test_goxave"])


@pytest.fixture
def product() -> Product:
    return Product(
        url="https://test-goxave.com/products/123",
        product_name="test product",
        product_price="₱999.99",
    )


@pytest.fixture
def product_with_invalid_currency() -> Product:
    return Product(
        url="https://test-goxave.com/products/123",
        product_name="test product",
        product_price="INVALID_CURRENCY999.99",
    )


@pytest.fixture
def product_with_no_currency() -> Product:
    return Product(
        url="https://test-goxave.com/products/123",
        product_name="test product",
        product_price="999.99",
    )


@pytest.fixture
def user_repository(mongodb_session, get_client):
    return UserRepository(mongodb_session, get_client["test_goxave"])


@pytest.fixture
def join_date():
    return 175793086.1234


@pytest.fixture
def user(join_date) -> User:
    return User(
        name="tester_name",
        email="test@email.com",
        join_date=join_date,
        current_session="session123",
        discord_webhook=os.environ["ADMIN_DISCORD_WEBHOOK"],
    )


@pytest.fixture
def login_repository(mongodb_session, get_client):
    return LoginRepository(mongodb_session, get_client["test_goxave"])


@pytest.fixture
def login() -> Login:
    return Login(session_id="session123", token="test_my_token")


@pytest.fixture
def uow(get_client):
    yield UnitOfWork(client=get_client, db_name="test_goxave")

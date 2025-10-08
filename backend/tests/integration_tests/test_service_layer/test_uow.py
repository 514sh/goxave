import pytest


def test_uow_saves_transaction_on_commit(uow, product, login, user):
    with uow:
        uow.logins.add(login)
        uow.users.add(user)
        uow.products.add(product)
        uow.commit()

    with uow:
        found_login = uow.logins.get(login)
        found_user = uow.users.get(user)
        found_product = uow.products.get(product)
        uow.commit()

    assert found_login.session_id == login.session_id
    assert found_user.email == user.email
    assert found_product.url == product.url


def test_uow_rollbacks_automatically_uncommited_transactions(uow, product, login, user):
    with uow:
        uow.logins.add(login)
        uow.users.add(user)
        uow.products.add(product)

    with uow:
        found_login = uow.logins.get(login)
        found_user = uow.users.get(user)
        found_product = uow.products.get(product)
        uow.commit()

    assert found_login is None
    assert found_user is None
    assert found_product is None


def test_uow_rollbacks_automatically_in_case_of_an_error(uow, product, login, user):
    class TestException(Exception):
        pass

    with pytest.raises(TestException):
        with uow:
            uow.products.add(product)
            uow.logins.add(login)
            uow.users.add(user)
            raise TestException()

    with uow:
        found_product = uow.products.get(product)
        found_user = uow.users.get(user)
        found_login = uow.logins.get(login)

    assert found_product is None
    assert found_user is None
    assert found_login is None

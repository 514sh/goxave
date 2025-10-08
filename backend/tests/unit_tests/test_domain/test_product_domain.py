from goxave.api.domain.events import (
    NotifyAdminRegardingProduct,
    NotifyUserOnPriceChange,
)


def test_price_change_event_added_when_previous_price_is_greater_than_current_price(
    product,
):
    current_price = "₱899.99"
    product.add_price_history(current_price)

    events = product.events

    assert len(events) == 1
    assert isinstance(events[0], NotifyUserOnPriceChange)
    assert len(product.price_history) == 2


def test_price_change_event_added_when_previous_price_is_less_than_current_price(
    product,
):
    current_price = "₱1099.99"
    product.add_price_history(current_price)

    events = product.events

    assert len(events) == 1
    assert isinstance(events[0], NotifyUserOnPriceChange)
    assert len(product.price_history) == 2


def test_no_price_change_event_added_when_previous_price_is_equal_to_the_current_price(
    product,
):
    current_price = "₱999.99"
    product.add_price_history(current_price)

    events = product.events

    assert len(events) == 0
    assert len(product.price_history) == 2


def test_product_currency_not_in_currency_codes_set(product_with_invalid_currency):
    events = product_with_invalid_currency.events

    assert len(events) == 1
    assert isinstance(events[0], NotifyAdminRegardingProduct)


def test_product_no_currency(product_with_no_currency):
    events = product_with_no_currency.events

    assert len(events) == 1
    assert isinstance(events[0], NotifyAdminRegardingProduct)

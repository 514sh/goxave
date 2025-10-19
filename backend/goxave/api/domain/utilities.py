import uuid
from datetime import datetime

from goxave.utilities.currencies import currency_codes, currency_symbols_set


def unix_millis(timestamp=None) -> int:
    if timestamp is None:
        timestamp = datetime.now().timestamp()
    return int(timestamp * 1000)


def url_id(url) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, url))


def dns_id(email) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, email))


def session_id():
    return str(uuid.uuid4())


def get_date_time() -> str:
    now = datetime.now()
    return datetime.strftime(now, "%Y/%m/%d %H:%M:%S.%f")


# https://wise.com/gb/blog/world-currency-symbols
def get_currency_symbol(value: str) -> str | None:
    my_currency = ""
    currency_codes_dict = currency_codes()
    currency_symbols = currency_symbols_set()
    if isinstance(value, str) and value in currency_symbols:
        my_currency = value
    elif isinstance(value, str) and value in currency_codes_dict:
        my_currency = currency_codes_dict[value]
    elif not isinstance(my_currency, str) or not my_currency:
        my_currency = None
    return my_currency

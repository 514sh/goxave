from google.auth.exceptions import InvalidValue
from google.auth.transport import requests
from google.oauth2 import id_token


def verify_token(token: str, audience: str) -> dict | None:  # -> None | Any | Any:
    request = requests.Request()
    try:
        id_info = id_token.verify_firebase_token(
            token,
            request,
            audience=audience,
        )
    except InvalidValue:
        return None
    return id_info

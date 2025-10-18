from goxave.api.auth import verify_token  # noqa: F401
from goxave.api.domain import commands, model, utilities  # noqa: F401
from goxave.api.service_layer import message_bus  # noqa: F401
from goxave.config import (  # noqa: F401
    FIREBASE_AUTH_PROJECT_ID,
    LIMIT_PER_HOUR,
    LIMIT_PER_MIN,
    LIMIT_PER_SEC,
    PROXY_URL,
    RATE_LIMIT_DISABLED,
    REDIS_HOST,
    REDIS_PORT,
    uow,
)
from goxave.tasks import ping_pong, scraper  # noqa: F401
from goxave.tasks.scraper import do_scrape_web  # noqa: F401
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    strategy="fixed-window",
    storage_uri="redis://{REDIS_HOST}:{REDIS_PORT}",
    enabled=not bool(RATE_LIMIT_DISABLED),
)

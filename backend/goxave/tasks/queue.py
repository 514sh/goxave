from celery import Celery
from celery.exceptions import MaxRetriesExceededError  # noqa: F401

from goxave.config import REDIS_HOST, REDIS_PORT

queue = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    include=["goxave.tasks.ping_pong", "goxave.tasks.scraper"],
)

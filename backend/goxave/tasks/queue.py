from celery import Celery
from celery.schedules import crontab

from goxave.config import INTERVAL_HOUR, INTERVAL_MIN, REDIS_HOST, REDIS_PORT


def get_schedule(minute=INTERVAL_MIN, hour=INTERVAL_HOUR) -> crontab:
    if hour == "0" or not hour:
        return crontab(minute=INTERVAL_MIN)
    return crontab(minute=minute, hour=hour)


queue = Celery(
    "tasks",
    broker=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    backend=f"redis://{REDIS_HOST}:{REDIS_PORT}/0",
    include=[
        "goxave.tasks.ping_pong",
        "goxave.tasks.scraper",
    ],
)

queue.conf.beat_schedule = {
    # "test-scheduler": {
    # "task": "goxave.tasks.scraper.test_print",
    # "schedule": 20.0,
    # "args": (),
    # },
    "scheduled-scrape": {
        "task": "goxave.tasks.scraper.scheduled_scrape",
        "schedule": get_schedule(),
        "args": (),
    },
}

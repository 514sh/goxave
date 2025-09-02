import os

from celery import Celery
from datetime import datetime

REDIS_PORT = os.environ["REDIS_PORT"]

queue = Celery("tasks", broker=f"redis://redis:{REDIS_PORT}/0", backend=f"redis://redis:{REDIS_PORT}/0")

def get_date_time():
  now = datetime.now()
  return datetime.strftime(now, "%Y/%m/%d %H:%M:%S.%f")

@queue.task(bind=True)
def ping_pong(self):
  return f"pong {get_date_time()} [{self.request.id}]"




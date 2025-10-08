from goxave.tasks.queue import queue


@queue.task(bind=True)
def ping_pong(self, pong_id, date_time) -> str:
    return f"pong {date_time} [{pong_id}]"

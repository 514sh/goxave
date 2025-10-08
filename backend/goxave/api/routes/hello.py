import asyncio

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from goxave.common import ping_pong, utilities

router = APIRouter(prefix="/api")


async def ping_pong_generator():
    ping_id = utilities.session_id()
    yield f"[{ping_id}] ping {utilities.get_date_time()}\t"
    after = utilities.get_date_time()
    result = ping_pong.ping_pong.delay(pong_id=ping_id, date_time=after)  # type: ignore
    i = 0
    while i < 20:
        if result.ready():
            yield result.get()
            break
        await asyncio.sleep(0.5)
        i += 1


@router.get("/hello")
def hello():
    return "Hello"


@router.get("/ping")
async def get_ping_pong():
    return StreamingResponse(ping_pong_generator(), media_type="text/event-stream")

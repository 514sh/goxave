from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from goxave.api import middleware
from goxave.api.routes import hello, login, product, user
from slowapi.errors import RateLimitExceeded

app = FastAPI()
# app.add_middleware(SessionMiddleware, secret_key="secret_key")
app.add_middleware(middleware.ValidateSessionMiddleware)


async def custom_rate_limit_handler(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    limit_detail = exc.detail.lower()
    retry_after = ""
    if "minute" in limit_detail:
        retry_after = " after a minute"
    elif "hour" in limit_detail:
        retry_after = " after an hour"
    return JSONResponse(
        status_code=429,
        content={
            "type": "error",
            "message": f"You've sent too many requests. Please wait and try again{retry_after}.",
            "detail": exc.detail,  # Includes SlowAPI's default limit info
            "redirect": "/",
        },
    )


app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)  # type: ignore

app.include_router(hello.router)
app.include_router(login.router)
app.include_router(product.router)
app.include_router(user.router)

app.include_router(user.router)

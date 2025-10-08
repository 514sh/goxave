from fastapi import FastAPI

from goxave.api import middleware
from goxave.api.routes import hello, login, product, user

app = FastAPI()
# app.add_middleware(SessionMiddleware, secret_key="secret_key")
app.add_middleware(middleware.ValidateSessionMiddleware)

app.include_router(hello.router)
app.include_router(login.router)
app.include_router(product.router)
app.include_router(user.router)

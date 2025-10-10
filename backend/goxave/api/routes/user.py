from typing import Annotated

from fastapi import APIRouter, Body, Request
from fastapi.responses import JSONResponse, RedirectResponse

from goxave.common import commands, message_bus, model, uow

router = APIRouter(prefix="/api")


@router.post("/users")
def add_my_discord_webhook(
    request: Request, discord_webhook: Annotated[str, Body(embed=True)]
):
    user_id = request.headers.get("user_id", "")
    user_model = model.User(id=user_id, discord_webhook=discord_webhook)
    handle_update_user_info = commands.UpdateUserInfo(user=user_model)
    is_successful = message_bus.handle(handle_update_user_info, uow)
    my_response = [None]
    if isinstance(is_successful, list) and len(is_successful) > 0:
        my_response = is_successful[0]
    if my_response is None:
        return JSONResponse(
            status_code=500, content={"message": "Unable to fetch your products."}
        )
    return RedirectResponse(url="/api/users", status_code=303)


@router.get("/users")
def get_user_info(request: Request):
    user_id = request.headers.get("user_id", "")
    user_model = model.User(id=user_id)
    handle_fetch_user_info = commands.FetchUserInfo(user=user_model)
    is_successful = message_bus.handle(handle_fetch_user_info, uow)
    my_response = [None]
    if isinstance(is_successful, list) and len(is_successful) > 0:
        my_response = is_successful[0]

    if isinstance(my_response, model.User):
        return JSONResponse(
            status_code=200,
            content={
                "user_id": my_response.dns_id,
                "email": my_response.email,
                "name": my_response.name,
                "discord_webhook": my_response.discord_webhook,
            },
        )
    return JSONResponse(
        status_code=500, content={"message": "Unable to fetch your products."}
    )

from typing import Annotated

from fastapi import APIRouter, Header, Request, Response
from fastapi.responses import JSONResponse, RedirectResponse, Response

from goxave.common import (
    FIREBASE_AUTH_PROJECT_ID,
    commands,
    message_bus,
    model,
    uow,
    utilities,
    verify_token,
)

router = APIRouter(prefix="/api")


@router.post("/login")
async def login(
    authorization: Annotated[str, Header()], response: Response
) -> RedirectResponse:
    session_id = utilities.session_id()
    token = ""
    if len(authorization) > 7:
        token = authorization[7:]
    token_verified = verify_token(token, audience=FIREBASE_AUTH_PROJECT_ID)
    valid_token = False
    detail_response = ""

    is_successful = False
    name, email = "", ""
    if token_verified:
        name = token_verified["name"]
        email = token_verified["email"]
    else:
        detail_response = "Invalid Token"

    login_model = model.Login(session_id=session_id, token=token)
    user_model = model.User(name=name, email=email, current_session=session_id)
    handle_login = commands.AddNewLogin(login=login_model, user=user_model)
    is_successful = message_bus.handle(handle_login, uow)
    my_response = [None]
    with_discord = False
    if isinstance(is_successful, list) and len(is_successful) > 0:
        my_response = is_successful[0]
    if my_response is None:
        detail_response = "Unable to login at this moment."
    elif isinstance(my_response, model.User) and my_response.discord_webhook:
        with_discord = True

    if not detail_response:
        detail_response = "Successfully logged in."
        valid_token = True

    response = RedirectResponse(
        f"/api/login?redirect=true&valid_token={valid_token}&message={detail_response}&with_discord={with_discord}",
        status_code=303,
    )

    response.set_cookie(key="session_id", value=session_id)
    return response


@router.get("/login")
async def validate_login(
    request: Request,
    redirect: bool = False,
    valid_token: bool = False,
    with_discord: bool = False,
    message: str = "",
) -> JSONResponse:
    if redirect:
        status_code = 400
        if valid_token:
            status_code = 201
        return JSONResponse(
            status_code=status_code,
            content={
                "type": "success",
                "message": message,
                "valid_token": valid_token,
                "with_discord": with_discord,
            },
        )
    session_id = request.cookies.get("session_id")
    with_discord = bool(getattr(request.state, "discord_webhook", None))
    if not session_id:
        return JSONResponse(
            status_code=401,
            content={
                "type": "error",
                "message": "No session provided",
                "valid_token": False,
            },
        )
    login_result = None
    with uow:
        login_model = model.Login(session_id=session_id)
        login_result = uow.logins.get(login_model)

    if not login_result:
        return JSONResponse(
            status_code=401,
            content={
                "type": "error",
                "message": "Invalid Session.",
                "valid_token": False,
            },
        )
    token_verified = verify_token(login_result.token, audience=FIREBASE_AUTH_PROJECT_ID)
    if not token_verified:
        return JSONResponse(
            status_code=401,
            content={"type": "error", "detail": "Invalid token", "valid_token": False},
        )

    return JSONResponse(
        status_code=200,
        content={
            "valid_token": not login_result.isLoggedOut,
            "with_discord": with_discord,
        },
    )


@router.delete("/login")
async def invalidate_login(request: Request) -> Response:
    session_id = request.cookies.get("session_id")
    if not session_id:
        return Response(status_code=204)

    with uow:
        login_model = model.Login(session_id=session_id)
        uow.logins.invalidate(login_model)
        uow.commit()

    response = Response(status_code=204)
    response.set_cookie("session_id", "")
    return response

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from goxave.common import FIREBASE_AUTH_PROJECT_ID, model, uow, verify_token


class ValidateSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.url.path.startswith("/api/login"):
            # Skip session validation for login route
            return await call_next(request)

        session_id = request.cookies.get("session_id")
        if not session_id:
            return JSONResponse(
                status_code=401, content={"message": "No session provided"}
            )
        login_result = None
        with uow:
            login_model = model.Login(session_id=session_id)
            login_result = uow.logins.get(login_model)
            uow.commit()

        if not login_result:
            raise Exception("Invalid session")
        token_verified = verify_token(
            login_result.token, audience=FIREBASE_AUTH_PROJECT_ID
        )
        if not token_verified:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        name = token_verified["name"]
        email = token_verified["email"]

        user_model = model.User(name=name, email=email, current_session="")
        current_user = None
        with uow:
            current_user = uow.users.get(user_model)
            uow.commit()
        if current_user and current_user.email == email:
            request.state.user_id = current_user.dns_id
            request.state.user_namae = current_user.name
            request.state.user_email = current_user.email
            request.state.discord_webhook = ""
            if current_user.discord_webhook:
                request.state.discord_webhook = current_user.discord_webhook
            response = await call_next(request)
            return response

        return JSONResponse(
            status_code=401, content={"detail": "Invalid user or session"}
        )

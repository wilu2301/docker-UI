from http import HTTPStatus

from fastapi import APIRouter,Response
from starlette.responses import JSONResponse

import backend.functions.auth
from backend import config
from backend.db.models import User
from backend.functions.auth import get_user_by_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def index():
    return {"message": "Welcome to FastAPI!"}


@router.post("/login")
async def login(username: str, password: str):
    user: User = backend.functions.auth.login(username, password)

    if user is None:
        return Response(status_code=401)

    data = backend.functions.auth.get_cookie(user)

    token = data["token"]
    ttl = data["ttl"]

    response = JSONResponse({
        "login": user.username,
        "token": token,
        "ttl": ttl,
    })
    response.set_cookie(key = "session", value = token, expires= config.COOKIE_LIFETIME)
    response.status_code = HTTPStatus.OK
    return response



@router.post("/create_user")
async def create_user(username: str, password: str):
    success = backend.functions.auth.create_user(username, password)
    if not success:
        return Response(status_code=400)
    return Response(status_code=200)


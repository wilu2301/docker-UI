from http import HTTPStatus

from fastapi import APIRouter,Response, Cookie
from starlette.responses import JSONResponse

import backend.db.engine as db
from backend.db.engine import engine
from backend.db.models import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def index():
    return



@router.post("/login")
async def login(username: str, password: str):
    user: User = db.login(username, password)

    if user is None:
        return Response(status_code=401)

    data = db.get_cookie(user)

    token = data["token"]
    ttl = data["ttl"]

    response = JSONResponse({
        "login": user.username,
        "token": token,
        "ttl": ttl,
    })
    response.set_cookie(key = "session", value = token, expires= ttl)
    response.status_code = HTTPStatus.OK
    return response



@router.post("/create_user")
async def create_user(username: str, password: str):
    success = db.create_user(username, password)
    if not success:
        return Response(status_code=400)
    return Response(status_code=200)


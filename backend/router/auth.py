from fastapi import APIRouter

import backend.db.engine as db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def index():
    return {"message": "Welcome to FastAPI!"}


@router.post("/create_user")
async def create_user(username: str, password: str):
    db.create_user(username, password)
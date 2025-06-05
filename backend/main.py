import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.functions import setup
from backend.router import auth, container
from backend.router.create import apps as apps_setup
from backend.router import apps
from backend.db import engine

app = FastAPI()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.on_event("startup")
def on_startup():
    engine.create_db_tables()
    logger.info("Database tables created")
    setup.startup_check()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return FileResponse(os.path.join("static", "index.html"))


# Redirect unmatched routes to index.html for SPA
@app.exception_handler(StarletteHTTPException)
async def spa_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return FileResponse(os.path.join("static", "index.html"))
    raise exc


app.include_router(auth.router, prefix="/api")
# app.include_router(container.router, prefix="/api")
# app.include_router(apps_setup.router, prefix="/api")
app.include_router(apps.router, prefix="/api")

# Add the resources for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

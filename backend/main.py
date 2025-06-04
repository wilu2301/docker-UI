import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

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

)


@app.get("/")
async def index():
    return FileResponse(os.path.join("static", "index.html"))



app.include_router(auth.router,prefix="/api")
app.include_router(container.router, prefix="/api")
app.include_router(apps_setup.router, prefix="/api")
app.include_router(apps.router, prefix="/api")

# Add the resources for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

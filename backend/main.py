
from fastapi import FastAPI
from fastapi.middleware.cors import  CORSMiddleware
from backend.router import auth, container, apps
from backend.db import engine
app = FastAPI()

@app.on_event("startup")
def on_startup():
    engine.create_db_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(container.router)
app.include_router(apps.router)

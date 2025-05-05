from fastapi import FastAPI
from backend.router import auth
from backend.db import engine
app = FastAPI()

@app.on_event("startup")
def on_startup():
    engine.create_db_tables()

app.include_router(auth.router)

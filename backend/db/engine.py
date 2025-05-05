from sqlmodel import create_engine, SQLModel
import logging

from backend import config

logging.getLogger("sqlmodel.engine").setLevel(logging.INFO)

engine = create_engine(config.DB_CONNECTION_STRING, echo=config.DEBUG)

def create_db_tables():
    SQLModel.metadata.create_all(engine)
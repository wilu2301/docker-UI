from sqlmodel import create_engine, SQLModel
import logging

from backend import config

logger = logging.getLogger(__name__)

engine = create_engine(config.DB_CONNECTION_STRING, echo=config.DEBUG)


def create_db_tables():
    SQLModel.metadata.create_all(engine)

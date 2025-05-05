from sqlalchemy import Select
from sqlmodel import create_engine, SQLModel, Session, select
from passlib.hash import bcrypt
import logging

from backend.db.models import User
from backend import config

logging.getLogger("sqlmodel.engine").setLevel(logging.INFO)

engine = create_engine(config.DB_CONNECTION_STRING, echo=config.DEBUG)

def create_db_tables():
    SQLModel.metadata.create_all(engine)


def create_user(username: str, password: str) -> bool:
    """
    Create a new user
    :param username: the username
    :param password: the password
    :return: success
    """

    hasher = bcrypt.using(rounds=13)

    new_user: User = User(
        username=username,
        password= hasher.hash(password)
    )

    with Session(engine) as session:
        # check if username is taken
        statement: Select = select(User).where(User.username == username)
        if len(session.exec(statement).all()) <= 0:
            session.add(new_user)
            logging.info(f"Created new user {username}")
            session.commit()
            session.close()
            return False
        else:
            logging.warning(f"User {username} already exists")
            session.close()
            return True




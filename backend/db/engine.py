import datetime
import random
from typing import Any

from sqlalchemy import Select
from sqlmodel import create_engine, SQLModel, Session, select
from passlib.hash import bcrypt
import logging

from backend.db.models import User, Token
from backend import config

logging.getLogger("sqlmodel.engine").setLevel(logging.INFO)


hasher = bcrypt.using(rounds=13)
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

def login(username, password) -> User | None:
    """
    Validate a user's password
    :param username: username
    :param password: password
    :return: the logged in user
    """
    with Session(engine) as session:
        statement_get_user: Select = select(User).where(User.username == username)

        selected_user = session.exec(statement_get_user).one()

        if hasher.verify(password, selected_user.password):
            logging.info(f"User {username} logged in")
            success = True
        else:
            logging.warning(f"User {username} password incorrect")
            success = False

        session.close()

        if success:
            return selected_user
        else:
            return None


def generate_cookie(associate_user: User) -> dict[str, str | int]:
    """
    Generates a new session token
    :param associate_user:
    :return:
    """

    # Generate a secret token

    time = datetime.datetime.now()
    rand = random.SystemRandom()

    token_str = hasher.hash(str(time.timestamp()) * random.randint(1,1000)
                        + associate_user.password
                        + str(rand.random())
                        )

    # Save the token to the db

    time_to_live: int = time.timestamp() + config.COOKIE_LIFETIME

    token = Token(token=token_str, user_id=associate_user.id,ttl = time_to_live)

    with Session(engine) as session:
        session.add(token)
        session.commit()
        session.close()
    return {"token": token_str, "ttl": time_to_live}



def get_cookie(associated_user: User) -> dict[str, str | int] | Any:
    """
    Gets a session cookie
    :param associated_user:
    :return: Session string
    """

    # Check if the user already has a cookie

    with Session(engine) as session:
        statement: Select = select(Token).where(Token.user_id == associated_user.id)
        result = session.exec(statement).one_or_none()

        if result is not None:
             return {"token": result.token, "ttl": result.ttl}

        else:
            return generate_cookie(associated_user)



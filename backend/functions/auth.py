import datetime
import logging
import random
from typing import Any

from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import Select
from sqlmodel import Session, select

from backend import config
from backend.db.engine import engine
from backend.db.models import User, Token


logger = logging.getLogger(__name__)

hasher = bcrypt.using(rounds=13)


def validate_scope(user_scope: int, required_scope: int) -> bool:
    """
    Validates scope
    :param user_scope:
    :param required_scope:
    :return: Permission
    """
    logger.debug(f"user_scope: {user_scope}")
    logger.debug(f"required_scope: {required_scope}")

    if user_scope & required_scope == required_scope:
        return True
    else:
        return False


def create_user(username: str, password: str) -> bool:
    """
    Create a new user
    :param username: the username
    :param password: the password
    :return: success
    """
    new_user: User = User(username=username, password=hasher.hash(password))

    with Session(engine) as session:
        # check if username is taken
        statement: Select = select(User).where(User.username == username)
        if len(session.exec(statement).all()) <= 0:
            session.add(new_user)
            logger.info(f"Created new user {username}")
            session.commit()
            session.close()
            return False
        else:
            logger.warning(f"User {username} already exists")
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

        selected_user = session.exec(statement_get_user).one_or_none()

        if selected_user is None:
            success = False
        else:
            if hasher.verify(password, selected_user.password):
                logger.info(f"User {username} logged in")
                success = True
            else:
                logger.warning(f"User {username} password incorrect")
                success = False

        if success:
            return selected_user
        else:
            return None


def generate_token(associate_user: User) -> dict[str, str | int]:
    """
    Generates a new session token
    :param associate_user:
    :return:
    """

    # Generate a secret token

    time = datetime.datetime.now()
    rand = random.SystemRandom()

    token_str = hasher.hash(
        str(time.timestamp()) * random.randint(0, 1)
        + associate_user.password
        + str(rand.random())
    )

    # Save the token to the db

    time_to_live: int = int(time.timestamp() + config.COOKIE_LIFETIME)

    token = Token(token=token_str, user_id=associate_user.id, ttl=time_to_live)

    with Session(engine) as session:
        session.add(token)
        session.commit()
        session.close()
    return {"token": token_str, "ttl": time_to_live}


def clear_token(token: str):
    with Session(engine) as session:
        statement: Select = select(Token).where(Token.token == token)
        selected_token = session.exec(statement).one_or_none()

        if selected_token is None:
            return

        session.delete(selected_token)
        session.commit()
        session.close()


def get_token(associated_user: User) -> dict[str, str | int] | Any:
    """
    Gets a session token
    :param associated_user:
    :return: Session string
    """

    # Check if the user already has a token

    with Session(engine) as session:
        statement: Select = select(Token).where(Token.user_id == associated_user.id)
        result = session.exec(statement).one_or_none()

        session.close()
        if result is not None:
            # Check if token is still valid

            time = datetime.datetime.now()

            if time.timestamp() > result.ttl:
                clear_token(result.token)
                return generate_token(associated_user)

            else:
                return {"token": result.token, "ttl": result.ttl}

        else:
            return generate_token(associated_user)


def get_user_by_token(token: str) -> User | None:
    """
    Gets user details by token
    :param token:
    :return:
    """

    # Check who owns the token

    success: bool = True

    with Session(engine) as session:
        statement: Select = select(Token).where(Token.token == token)

        token_data: Token | None = session.exec(statement).one_or_none()

        if token_data is None:
            success = False
        else:
            user_id: int | None = token_data.user_id
            ttl: int | None = token_data.ttl

        # Check if the token is still valid

        time = datetime.datetime.now()

        if success:
            if time.timestamp() > ttl:
                clear_token(token)
                success = False

    if success:
        # Get user data
        statement: Select = select(User).where(User.id == user_id)

        user = session.exec(statement).one_or_none()

        if user is None:
            success = False
    session.close()
    if success:
        # noinspection PyUnboundLocalVariable
        return user
    else:
        return None


def has_permission(token, scope: int) -> bool:
    """
    Checks if a token is authenticated and the scope is valid
    :param token: session token
    :param scope: user scope
    :return: authenticated or not
    """

    # Get the user
    selected_user = get_user_by_token(token)

    if selected_user is None or selected_user.scope is None:
        return False

    if not validate_scope(required_scope=scope, user_scope=selected_user.scope):
        return False

    return True

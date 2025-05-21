import logging
import pathlib
from datetime import datetime

from git import Repo, GitCommandError
from sqlalchemy import Select
from sqlmodel import Session, select

from backend import config
from backend.db.engine import engine
from backend.db.models import User, AppSetup, Apps, Ports
from backend.functions.auth import get_user_by_token
from backend.functions.utils import is_folder_name_allowed


def get_editing_user_id_creation_app(user: User) -> int:
    """
    Get the editing user id of the creating app.
    :param user: The user that is creating the app.
    :return: The editing user id.
    """

    user_id = user.id if user else -1

    # Check if the user already has an app
    with Session(engine) as session:
        statement: Select = select(AppSetup).where(AppSetup.editing_user_id == user_id)
        result = session.exec(statement).one_or_none()
        if result is None:

            logging.warning("Creating new app in creation database")
            app = AppSetup(editing_user_id=user.id, creation_time=datetime.now())
            session.add(app)
            session.commit()
            return user_id
        else:
            return result.editing_user_id


def write_to_creation_db(name = None, git = False ,git_url = None,
                         git_branch = None, git_username = None, git_token = None, git_folder = None, editing_user = None):
    """
    Write the app creation data to the database.
    :param editing_user:
    :param git: If the app uses git.
    :param name: App name.
    :param git_url: Git repository url.
    :param git_branch: Git branch.
    :param git_username: Git username.
    :param git_token: Git token.
    :param git_folder: Git folder.
    """

    # Create a new app in the creation database

    if editing_user is None:
        return

    editing_user_id = get_editing_user_id_creation_app(editing_user)

    with Session(engine) as session:
        # Edit the app in the creation database
        statement: Select = select(AppSetup).where(AppSetup.editing_user_id == editing_user_id)
        app = session.exec(statement).first()
        if app:
            app.name = name if name else app.name
            app.git = git if git else app.git
            app.git_url = git_url if git_url else app.git_url
            app.git_branch = git_branch if git_branch else app.git_branch
            app.git_username = git_username if git_username else app.git_username
            app.git_token = git_token if git_token else app.git_token
            app.git_folder = git_folder if git_folder else app.git_folder

            session.add(app)
        session.commit()


def get_creation_data(editing_user: User) -> dict:
    """
    Get the app creation data from the database.
    :param editing_user: The user that is creating the app.
    :return: The app creation data.
    """

    if editing_user is None:
        return {}

    with Session(engine) as session:
        statement: Select = select(AppSetup).where(AppSetup.editing_user_id == editing_user.id)
        result = session.exec(statement).one_or_none()
        if result is None:
            return {}
        else:

            return result.dict()


def get_app_id_by_token(token: str) -> int | None:
    """
    Get the app id by token.
    :param token: The token of the user.
    :return: The app id.
    """

    return get_editing_user_id_creation_app(get_user_by_token(token))


def check_name_available(name: str) -> bool:
    """
    Check if the name is available.
    :param name: Name to check.
    :return: True if the name is available, False otherwise.
    """

    if not is_folder_name_allowed(name):
        return False


    with Session(engine) as session:
        statement: Select = select(Apps).where(Apps.name == name)
        if len(session.exec(statement).all()) <= 0:
            return True
        else:
            return False


def git_connection(name: str,git_url: str, git_folder="/main", git_branch="main", git_username=None, git_token=None, editing_user=None) -> dict:
    """
    Test connection to the git repository and adds it to the AppsSetup table.
    :param editing_user: The user that is creating the app.
    :param name: App name.
    :param git_url: Git repository url.
    :param git_folder: Git folder.
    :param git_branch: Git branch.
    :param git_username: Git username.
    :param git_token: Git token.
    :return: A dictionary with the status and message.
    """

    if not check_name_available(name): return {"status": False, "type": "name"}

    write_to_creation_db(editing_user=editing_user, git=True, name=name, git_url=git_url, git_branch=git_branch,
                         git_username=git_username, git_token=git_token, git_folder=git_folder)


    if git_username and git_token:
        protocol, rest = git_url.split("://")
        git_url = f"{protocol}://{git_username}:{git_token}@{rest}"

    # Check if a folder of the project already exists
    skip_clone  = False
    if pathlib.Path(f"{config.APP_STORAGE}/{name}").exists():
        skip_clone = True


    try:
        if  skip_clone:
            repo = Repo(f"{config.APP_STORAGE}/{name}")
        else:
            repo = Repo.clone_from(git_url, f"{config.APP_STORAGE}/{name}")
        repo.git.checkout(git_branch)

    except GitCommandError as e:
        if "already exists" in e.stderr:
            # Folder already exists
            pass
        elif "Could not resolve host" in e.stderr:
            # Invalid URL
            return {"status": False, "type": "url", "valid": ["name"]}
        elif "not found" in e.stderr:
            # Repository not found
            return {"status": False, "type": "url"}
        elif "pathspec" in e.stderr:
            # Branch not found
            return {"status": False, "type": "branch", "valid": ["name", "url"]}
            # Authentication failed
        if "Authentication failed" in e.stderr or "could not read Username" in e.stderr or "Permission" in e.stderr:
            return {"status": False, "type": "auth_clone", "valid": ["name", "url","branch"]}
        else:
            # Other error
            return {"status": False, "type": "other", "message": e.stderr}


    # Cloning was successful
    # Check if the user has write access to the repository
    try:
        repo.git.push("origin", git_branch)
    except GitCommandError as e:
        if "Authentication failed" in e.stderr or "could not read Username" in e.stderr or "Permission" in e.stderr:
            # User does not have write access
            print(e)
            return {"status": False, "type": "auth_push","valid": ["name", "url","branch","auth_clone"]}
        else:
            # Other error
            return {"status": False, "type": "other", "message": e.stderr}

    # Check if folder name is allowed
    if not is_folder_name_allowed(git_folder.replace("/","")):
        return {"status": False, "type": "folder", "valid": ["name", "url", "branch", "auth_clone", "auth_push"]}
    try:
        # Check if folder in git repository exists
        if not git_folder.startswith("/"):
            git_folder = "/" + git_folder

        if pathlib.Path(f"{config.APP_STORAGE}/{name}{git_folder}").exists():
            return {"status": False, "type": "folder_exists", "valid": ["name", "url", "branch", "auth_clone", "auth_push","folder"]}
    except OSError as e:
        return {"status": False, "type": "other", "message": e.strerror}


    return {"status": True, "message": None, "valid": ["name", "url", "branch", "auth_clone", "auth_push","folder"]}


def check_port_available(port: int) -> bool:
    """
    Check if the port is available.
    :param port: Host port to check.
    :return: True if the port is available, False otherwise.
    """

    # Check if port is in range:

    if port < 1 or port > 65535:
        return False

    with Session(engine) as session:
        statement: Select = select(Ports).where(Ports.host_port == port)
        if len(session.exec(statement).all()) <= 0:
            return True
        else:
            return False



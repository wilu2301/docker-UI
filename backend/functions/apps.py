from git import Repo, InvalidGitRepositoryError, GitCommandError
from sqlalchemy import Select
from sqlmodel import Session, select

from backend import config
from backend.db.engine import engine
from backend.db.models import Apps


def check_name_available(name: str) -> bool:
    """
    Check if the name is available.
    :param name: Name to check.
    :return: True if the name is available, False otherwise.
    """

    if name is None or name == "":
        return False

    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if any(char in name for char in invalid_chars):
        return False

    if len(name) > 20:
        return False



    with Session(engine) as session:
        statement: Select = select(Apps).where(Apps.name == name)
        if len(session.exec(statement).all()) <= 0:
            return True
        else:
            return False





def git_connection(name: str,git_url: str, git_folder="/", git_branch="main", git_username=None, git_token=None) -> dict:
    """
    Test connection to the git repository.
    :param name:
    :param git_url: Git repository url.
    :param git_folder: Git folder.
    :param git_branch: Git branch.
    :param git_username: Git username.
    :param git_token: Git token.
    :return: A dictionary with the status and message.
    """

    if not check_name_available(name): return {"status": False, "type": "name"}

    if git_username and git_token:
        protocol, rest = git_url.split("://")
        git_url = f"{protocol}://{git_username}:{git_token}@{rest}"



    try:
        repo = Repo.clone_from(git_url, config.APP_STORAGE + name)
        repo.git.checkout(git_branch)

    except GitCommandError as e:
        if "already exists" in e.stderr:
            # Folder already exists
            pass
        elif "Could not resolve host" in e.stderr:
            # Invalid URL
            return {"status": False, "type": "url"}
        elif "not found" in e.stderr:
            # Repository not found
            return {"status": False, "type": "url"}
        elif "pathspec" in e.stderr:
            # Branch not found
            return {"status": False, "type": "branch"}
            # Authentication failed
        if "Authentication failed" in e.stderr or "could not read Username" in e.stderr:
            return {"status": False, "type": "auth"}
        else:
            # Other error
            return {"status": False, "type": "other", "message": e.stderr}


    # Cloning was successful
    # Check if the user has write access to the repository
    try:
        repo.git.push("origin", git_branch)


    except GitCommandError as e:
        if "Authentication failed" in e.stderr:
            # User does not have write access
            return {"status": False, "type": "auth"}
        else:
            # Other error
            return {"status": False, "type": "other", "message": e.stderr}


    return {"status": True, "message": None}

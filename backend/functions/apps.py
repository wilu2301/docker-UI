from git import Repo
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





def git_connection(name: str,git_url: str, git_folder: str, git_branch:str, git_username: str, git_token:str) -> dict[bool, str]:
    """
    Test connection to the git repository.
    :param git_url: Git repository url.
    :param git_folder: Git folder.
    :param git_branch: Git branch.
    :param git_username: Git username.
    :param git_token: Git token.
    :return: A dictionary with the status and message.
    """

    Repo.clone_from(git_url, config.APP_STORAGE + git_folder, branch=git_branch, depth=1, single_branch=True)
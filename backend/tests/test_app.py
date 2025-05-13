import shutil

import pytest

from backend.db.models import User
from backend.functions.apps import git_connection
import pathlib
import dotenv


@pytest.fixture
def cleanup():
    """
    Cleanup function to remove the test folder.
    """

    yield
    if pathlib.Path("storage").exists():
        shutil.rmtree("storage")


def test_connection_clone_wrong_url(cleanup):
    """
    Test the test_connection with wrong URL.
    """

    git_url = "https://notAGitUrltest.git"

    result = git_connection("test", git_url)
    assert result["status"] == False
    assert result["type"] == "url"


def test_connection_clone_wrong_url_1(cleanup):
    """
    Test the test_connection with wrong URL.
    """

    git_url = "https://github.com/gitpython-developers/GitPythona.git"

    result = git_connection("test", git_url)
    assert result["status"] == False
    assert result["type"] == "url"


def test_connection_wrong_branch(cleanup):
    """
    Test the connection with a wrong branch.
    """

    git_url = "https://github.com/gitpython-developers/QuickStartTutorialFiles.git"
    branch = "wrong_branch"
    # Test the test_connection function

    dotenv.load_dotenv()
    git_username = dotenv.get_key("../.env", "GIT_TEST_USERNAME")
    git_token = dotenv.get_key("../.env", "GIT_TEST_TOKEN")

    result = git_connection("test", git_url, git_branch=branch, git_username=git_username, git_token=git_token)
    assert result["status"] == False
    assert result["type"] == "branch"



def test_connection_auth_fail(cleanup):
    """
    Test the connection with wrong credentials.
    """

    git_url = "https://github.com/wilu2301/test-auth.git"

    result = git_connection("test", git_url, git_username="1", git_token="1")
    assert result["status"] == False
    assert result["type"] == "auth_clone"





def test_connection_auth(cleanup):
    """
    Test the connection with valid credentials.
    """

    git_url = "https://github.com/wilu2301/test-auth.git"

    dotenv.load_dotenv()
    git_username = dotenv.get_key("../.env", "GIT_TEST_USERNAME")
    git_token = dotenv.get_key("../.env", "GIT_TEST_TOKEN")



    result = git_connection("test", git_url, git_username=git_username, git_token=git_token)
    assert result["status"] == True


def test_connection_valid_folder(cleanup):
    """
    Test the connection with valid folder.
    """

    git_url = "https://github.com/wilu2301/test-auth.git"

    dotenv.load_dotenv()
    git_username = dotenv.get_key("../.env", "GIT_TEST_USERNAME")
    git_token = dotenv.get_key("../.env", "GIT_TEST_TOKEN")

    result = git_connection("test", git_url, git_folder="/not-existent-folder", git_username=git_username,
                            git_token=git_token)
    assert result["status"] == True




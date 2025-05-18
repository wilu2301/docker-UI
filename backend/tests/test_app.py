import os
import shutil

import pytest

from backend.db.models import User
from backend.functions.apps import git_connection, write_to_creation_db, get_creation_data, check_port_available, \
    add_port, get_app_ports, delete_app_port, create_service
import pathlib
import dotenv


@pytest.fixture
def cleanup():
    """
    Cleanup function to remove the test folder.
    """

    # Copy the current database to the test folder
    if pathlib.Path("../database.db").exists():
        shutil.copyfile("../database.db", "database.db")


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


def test_connection_wrong_folder(cleanup):
    """
    Test the connection with a wrong folder.
    """

    git_url = "https://github.com/wilu2301/test-auth.git"

    dotenv.load_dotenv()
    git_username = dotenv.get_key("../.env", "GIT_TEST_USERNAME")
    git_token = dotenv.get_key("../.env", "GIT_TEST_TOKEN")

    result = git_connection("test", git_url, git_folder="/<Not allowed>", git_username=git_username,
                            git_token=git_token)
    assert result["status"] == False


def test_write_to_creation_db():
    """
    Test the write_to_creation_db function.
    """

    user = User(id=-100, username="test")
    write_to_creation_db(editing_user=user,name="test")


def test_read_from_creation_db():
    """
    Test the read_from_creation_db function.
    """

    user = User(id=-100, username="test")
    result = get_creation_data(editing_user=user)
    assert result["name"] == "test"


def test_check_port_available():
    """
    Test the check_port_available function.
    """

    port = 80
    result = check_port_available(port)
    assert result == True

    # Min port number is 1
    port = 0
    result = check_port_available(port)
    assert result == False

    # Max port number is 65535
    port = 65536
    result = check_port_available(port)
    assert result == False


def test_add_port(cleanup):
    result = add_port(-1, 80, 80, tcp=True, udp=False)

    assert result == True


    # Double binding ports
    result = add_port(-1, 80, 80, tcp=True, udp=False)
    assert result == False


def test_get_app_ports(cleanup):
    """
    Test the get_app_ports function.
    """

    # Add a port to the app
    port1 = add_port(-1, 80, 80, tcp=True, udp=False)
    assert port1 == True

    # Add a second port to the app
    port2 = add_port(-1, 81, 81, tcp=True, udp=False)
    assert port2 == True

    # Get the app ports
    result = get_app_ports(-1)

    assert result == [{'container_port': 80, 'udp': False, 'host_port': 80, 'tcp': True, 'app_id': -1, 'is_setup': False},
                      {'container_port': 81, 'udp': False, 'host_port': 81, 'tcp': True, 'app_id': -1, 'is_setup': False}]


def test_delete_app_port(cleanup):
    """
    Test the delete_app_port function.
    """

    # Add a port to the app
    port1 = add_port(-1,80, 80, tcp=True, udp=False)
    assert port1 == True

    # Delete the port
    result = delete_app_port(app_id=-1, host_port=80)
    assert result == True

    # Check if the port was deleted
    result = get_app_ports(-1)
    assert result == []

def test_create_service(cleanup):
    """
    Test the create_service function.
    """

    # Add a service to the app
    result = create_service(app_id=-1, container_name="test", container_image="test")
    assert result == True
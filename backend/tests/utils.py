import pathlib
import shutil

import pytest


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


@pytest.fixture
def create_test_app():
    pathlib.Path("storage/test_app").mkdir(parents=True, exist_ok=True)
    shutil.copyfile("compose/test-nginx.yml", "storage/test_app/docker-compose.yml")

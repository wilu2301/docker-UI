import os

from backend import config
from backend.functions.app.apps import get_app
import pathlib

from python_on_whales import docker

STORAGE = config.APP_STORAGE

def start_app(app_name) -> bool:
    """
    Starts the compose file for the app.
    :param app_name:
    :return: success
    """

    # Checks if app exists in db

    if get_app(app_name) is None:
        return False

    # Check if the app exists in storage
    if not pathlib.Path(f"{STORAGE}/{app_name}").exists():
        return False

    # Check if the compose file exists
    if not pathlib.Path(f"{STORAGE}/{app_name}/docker-compose.yml").exists():
        return False

    # Check if the compose file is a file
    if not pathlib.Path(f"{STORAGE}/{app_name}/docker-compose.yml").is_file():
        return False

    # Start the compose file
    try:
        docker.stack.deploy(name=app_name,compose_files=[f"{STORAGE}/{app_name}/docker-compose.yml"])
        return True
    except Exception as e:
        print(f"Error starting app: {e}")
        return False


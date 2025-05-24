"""
----- Docker Stack Handler -----
"""

import logging
from enum import Enum

from backend import config
import pathlib

from python_on_whales import docker, Stack

logger = logging.getLogger(__name__)

STORAGE = config.APP_STORAGE


class AppState(Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"
    UNKNOWN = "unknown"


def start_app(app_name) -> bool:
    """
    Starts the compose file for the app.
    :param app_name:
    :return: success
    """

    # Checks if app exists in db
    if get_app(app_name) is None:
        logger.warning(f"App '{app_name}' not found in db.")
        return False

    # Check if the app exists in storage
    if not pathlib.Path(f"{STORAGE}/{app_name}").exists():
        return False

    # Check if the compose file exists
    if not pathlib.Path(f"{STORAGE}/{app_name}/docker-compose.yml").exists():
        logger.warning(f"Compose file for app '{app_name}' not found.")
        return False

    # Check if the compose file is a file
    if not pathlib.Path(f"{STORAGE}/{app_name}/docker-compose.yml").is_file():
        logger.warning(f"Compose file for app '{app_name}' is not a file.")
        return False

    # Start the compose file
    try:
        docker.stack.deploy(
            name=app_name, compose_files=[f"{STORAGE}/{app_name}/docker-compose.yml"]
        )
        return True
    except Exception as e:
        logger.error(f"Error starting app '{app_name}': {e}")
        return False


def stop_app(app_name) -> bool:
    """
    Stops the compose file for the app.
    :param app_name:
    :return: success
    """

    # Check if the app is running

    if docker.stack.ps(app_name) is None:
        return False

    # Stop the stack
    try:
        docker.stack.remove(app_name)
        return True
    except Exception as e:
        logger.error(f"Error stopping app '{app_name}': {e}")
        return False


def get_app_state(app_name) -> AppState:
    """
    Get the state of the app from docker.
    :param app_name:
    :return:
    """

    # Check if the app is running
    if docker.stack.ps(app_name) is None:
        return AppState.STOPPED

    # TODO: Check if the app is running
    return AppState.RUNNING


def get_apps() -> list[Stack]:
    """
    Get all apps from docker.
    :return: list of apps
    """

    # Get all apps from docker
    try:
        stacks = docker.stack.list()
        return stacks
    except Exception as e:
        logger.error(f"Error getting apps: {e}")
        return []

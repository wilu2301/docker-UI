import logging

from backend.db.engine import engine
from backend.db.models import User
from docker import DockerClient

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    def __init__(self, message):
        logger.error(message)


def swarm_enabled() -> bool:
    """
    Check if Docker Swarm is enabled
    :return: True if Swarm is enabled, False otherwise
    """
    client = DockerClient.from_env()

    return client.info()["Swarm"]["LocalNodeState"] == "active"


def startup_check() -> None:
    """
    Check if the node is properly configured
    :return:
    """
    if not swarm_enabled():
        raise ConfigurationError("Docker Swarm is disabled")


def setup_database() -> None:
    """
    Creates a default user
    :return: None
    """

    user = User(
        username="admin",
        password="<PASSWORD>",
    )

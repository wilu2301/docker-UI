from docker import DockerClient
from backend.functions.setup import swarm_enabled


def test_swarm_enabled():
    """
    Test the swarm_enabled function.
    :return: None
    """

    DockerClient.from_env().swarm.leave("force")

    # Test with Docker Swarm disabled
    assert swarm_enabled() == False

    DockerClient.from_env().swarm.init()

    # Test with Docker Swarm enabled
    assert swarm_enabled() == True

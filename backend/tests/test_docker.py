import pytest

from backend.functions import docker


def test_get_all_containers():
    print(docker.get_all_containers())
    assert True


def test_pull_image():
    """
    Test the pull image function.
    """
    image = "nginx:latest"
    result = docker.pull_image(image)
    assert result == True


@pytest.mark.skip
def test_get_container():
    """
    Test the get container function.
    """
    container_id = "nginx-test"
    result = docker.get_container(container_id=container_id)
    assert result is not None


def test_get_container_logs():
    """
    Test the get container logs function.
    """
    container_id = "portainer"
    result = docker.get_container_logs(container_id=container_id)
    print(result)
    assert result is not None
    assert isinstance(result, str)  # Ensure logs are returned as a string

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
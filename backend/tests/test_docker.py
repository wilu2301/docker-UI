from backend.functions import docker


def test_get_all_containers():
    print(docker.get_all_containers())
    assert True
import docker

client = docker.from_env()


def get_all_containers() -> list[str]:
    """
    Gets all containers on the current client.
    :return: A list of container id's.
    """

    containers_id = []

    containers_query = client.containers.list()
    for container in containers_query:
        containers_id.append(container.id)

    return containers_id


def get_container(name: str = "", container_id: str = "") -> dict | None:
    """
    Gets a container by its name or id.
    :param name: Container name.
    :param container_id: Container id.
    :return: Container object.
    """

    if name == "":
        return client.containers.get(container_id).attrs
    if container_id == "":
        return client.containers.get(name).attrs

    return None


def pull_image(image: str) -> bool:
    """
    Pulls an image from the docker registry.
    :param image: The image to pull.
    :return: True if the image was pulled, False otherwise.
    """

    try:
        client.images.pull(image)
        return True
    except Exception as e:
        print(f"Error pulling image: {e}")
        return False

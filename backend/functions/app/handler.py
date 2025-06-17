"""
----- Docker Stack Handler -----
"""

import logging

from python_on_whales.components.service.models import EndpointPortConfig

from backend import config
from backend.functions.app import models as md
import pathlib

from python_on_whales import (
    docker,
    Stack,
    DockerException,
    Task,
    Container,
    Service,
    ContainerStats,
)


logger = logging.getLogger(__name__)

STORAGE = config.APP_STORAGE


def start_app(app_name) -> bool:
    """
    Starts the compose file for the app.
    :param app_name:
    :return: success
    """

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
    try:
        if len(docker.stack.ps(app_name)) == 0:
            return False
    except DockerException:
        return False

    # Stop the stack
    try:
        docker.stack.remove(app_name)
        return True
    except Exception as e:
        logger.error(f"Error stopping app '{app_name}': {e}")
        return False


def get_app_state(app_name) -> md.AppStatus:
    """
    Get the state of the app from docker.
    :param app_name:
    :return:
    """
    try:
        # Check if the app is running
        if docker.stack.ps(app_name) is None:
            return md.AppStatus.UNKNOWN

        # Get the services
        services: list[Task] = docker.stack.ps(app_name)

        if not services:
            return md.AppStatus.UNKNOWN

        num_stopped = 0
        for service in services:
            if service.status.state == "stopped":
                num_stopped += 1

        if num_stopped == 0:
            return md.AppStatus.RUNNING
        elif num_stopped == len(services):
            return md.AppStatus.STOPPED
        else:
            return md.AppStatus.DEGRADED

    except DockerException as e:
        logger.error(f"Error getting app state for '{app_name}': {e}")
        return md.AppStatus.UNKNOWN


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


def get_service_ports(service: Service) -> list[md.Port]:
    """
    Gets the ports exposed by the app.
    :param service: The service to get the ports from.
    :return:
    """

    ports_exposed: list[md.Port] = []
    ports: list[EndpointPortConfig] = service.endpoint.spec.ports
    if ports is None:
        logger.warning(f"No ports exposed for service '{service.id}'")
        return ports_exposed

    for port in ports:
        if port is not None:
            ports_exposed.append(
                md.Port(
                    container_port=port.target_port,
                    public_port=port.published_port,
                    tcp=port.protocol == "tcp",
                    udp=port.protocol == "udp",
                    ingress=port.publish_mode == "ingress",
                )
            )

    return ports_exposed


def get_app_volumes(app_name: str) -> list[md.Volume]:
    """
    Get the volumes used by the app.
    :param app_name: Name of the app.
    :return: List of volumes used by the app.
    """

    try:
        # Get the volumes used by the app
        volumes = docker.volume.list(filters={"name": app_name})

        if not volumes:
            return []

        return [
            md.Volume(
                name=volume.name,
                mountpoint=str(volume.mountpoint.resolve()),
                created_at=volume.created_at,
                driver=volume.driver,
            )
            for volume in volumes
        ]

    except DockerException as e:
        logger.error(f"Error getting app volumes for '{app_name}': {e}")
        return []


def get_app_usage(app_name) -> md.AppUsage | None:
    """
    Get the usage of the app.
    :return: AppUsage object
    """

    try:
        # Get the app services
        tasks: list[Task] = docker.stack.ps(app_name)

        if not tasks:
            return None

        service_ids: set[str] = set(task.service_id for task in tasks)

        containers: set[Container] = docker.container.list(
            filters={
                "name": app_name,
            }
        )

        stats: set[ContainerStats] = docker.stats(containers)

        # Calculate usage statistics
        cpu_usage = sum(stat.cpu_percentage for stat in stats)
        memory_usage = sum(stat.memory_percentage for stat in stats)
        # Round memory usage to 2 decimal places
        cpu_usage = round(cpu_usage, 2)
        memory_usage = round(memory_usage, 2)

        containers_running = len(containers)

        # Get the ports exposed
        ports_exposed: list[md.Port] = []

        for service_id in service_ids:
            service: Service = docker.service.inspect(service_id)
            ports_exposed.extend(get_service_ports(service))

        # Get the volumes count
        volumes_count = len(docker.volume.list(filters={"name": app_name}))

        return md.AppUsage(
            cpu_usage=int(cpu_usage),
            memory_usage=memory_usage,
            containers_running=containers_running,
            ports_exposed=ports_exposed,
            volumes_count=volumes_count,
        )

    except DockerException as e:
        logger.error(f"Error getting app usage for '{app_name}': {e}")
        return None


def get_node_name_by_id(node_id: str) -> str:
    """
    Get the node name by its ID.
    :param node_id: The ID of the node.
    :return: The name of the node.
    """
    try:
        node = docker.node.inspect(node_id)
        return node.description.hostname
    except DockerException as e:
        logger.error(f"Error getting node by ID '{node_id}': {e}")
        return "Unknown Node"


def get_app_service_names(app_name: str) -> list[str]:
    """
    Get the names of the services in the app.
    :param app_name: Name of the app.
    :return: List of service names.
    """
    try:
        # Get the services for the app
        tasks = docker.service.list(filters={"name": app_name})

        if not tasks:
            logger.warning(f"No services found for app '{app_name}'")
            return []

        return [task.spec.name for task in tasks]

    except DockerException as e:
        logger.error(f"Error getting app service names for '{app_name}': {e}")
        return []


def get_service_containers_overview(service_name: str) -> list[md.ContainerOverview]:
    """
    Get the containers overview for the app.
    :param service_name: Name of the sevice.
    :return: List of containers for the app.
    """

    try:
        # Get service containers

        tasks = docker.service.ps(service_name)

        if not tasks:
            logger.warning(f"No service found with name '{service_name}'")
            return []

        containers: list[Container] = []
        for task in tasks:
            containers.extend(docker.container.list(filters={"name": task.id}))

        if not containers:
            logger.warning(f"No containers found for app '{service_name}'")
            return []

        return [
            md.ContainerOverview(
                name=container.name,
                image=container.config.image,
                status=md.ContainerStatus(
                    container.state.status if container.state else "dead"
                ),
                node=get_node_name_by_id(
                    container.config.labels.get(
                        "com.docker.swarm.node.id", "Unknown Node"
                    )
                ),
            )
            for container in containers
        ]

    except DockerException as e:
        logger.error(f"Error getting app containers overview for '{service_name}': {e}")
        return []


def get_config_files(app_name: str) -> list[md.ConfigFile]:
    """
    Get the config files of the app.
    :param app_name: Name of the app.
    :return: Config files.
    """

    # Check if the app exists in storage
    if not pathlib.Path(f"{STORAGE}/{app_name}").exists():
        logger.warning(f"App '{app_name}' does not exist in storage.")
        return []

    # Get all files in the app directory

    files : list[md.ConfigFile] = []

    for file in pathlib.Path(f"{STORAGE}/{app_name}").iterdir():
        if file.is_file():
            files.append(
                md.ConfigFile(
                    name=file.name,
                    language=file.suffix[1:],
                    content=file.read_text(encoding="utf-8")
                )
            )

    return files


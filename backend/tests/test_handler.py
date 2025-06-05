import time

import pytest
from python_on_whales import docker, Service, DockerException

from backend.functions.app.handler import (
    start_app,
    stop_app,
    get_app_state,
    get_apps,
    get_app_usage,
    get_service_ports,
    get_app_volumes,
    get_service_containers_overview,
    get_node_name_by_id,
    get_app_service_names,
)
from backend.functions.app.models import Volume
from backend.tests.utils import cleanup, create_test_app
from backend.functions.app import models as md


@pytest.fixture()
def running_test_app(create_test_app, cleanup):
    """
    Fixture to create a running test app.
    :return: None
    """

    # Start the app
    start_app("test_app")

    yield

    # Stop the app
    stop_app("test_app")


def test_start_app(create_test_app, cleanup):
    """
    Test the start_app function.
    :return: None
    """
    # Test with a non-existing app
    assert start_app("non_existing_app") == False

    # Test with an existing app
    assert start_app("test_app") == True


def test_stop_app(running_test_app, cleanup):
    """
    Test the stop_app function.
    :return: None
    """
    # Test with a non-existing app
    assert stop_app("non_existing_app") == False

    # Test with an existing app
    assert stop_app("test_app") == True


def test_get_app(running_test_app, cleanup):
    """
    Test the get_app function.
    :return: None
    """
    time.sleep(1)  # Wait for the app to start

    # Test with a non-existing app
    assert get_app_state("non_existing_app") == md.AppStatus.UNKNOWN

    # Test with an existing app
    result = get_app_state("test_app")
    assert result == md.AppStatus.RUNNING


def test_get_apps(running_test_app, cleanup):
    """
    Test the get_apps function.
    :return: None
    """

    # Test with no apps
    result = get_apps()
    assert len(result) == 1
    assert result[0].name == "test_app"


@pytest.mark.xfail(reason="This test is flaky and needs to be fixed.")
def test_get_service_ports(running_test_app, cleanup):
    """
    Test the get_service_ports function.
    :return: None
    """

    time.sleep(2)  # Wait for the app to start

    result: list[md.Port] = []
    expected: list[md.Port] = [
        md.Port(public_port=8080, container_port=80, tcp=True, udp=False, ingress=True)
    ]

    service_ids: set[str] = set(task.service_id for task in docker.stack.ps("test_app"))

    for service_id in service_ids:
        service: Service = docker.service.inspect(service_id)
        result.extend(get_service_ports(service))

    assert result == expected


def test_get_app_usage(running_test_app, cleanup):
    """
    Test the get_app_usage function.
    :return: None
    """
    time.sleep(3)  # Wait for the app to start

    # Test with an existing app
    usage: md.AppUsage = get_app_usage("test_app")
    assert usage.cpu_usage >= 0
    assert usage.memory_usage >= float(0.0)
    assert usage.containers_running > 0
    assert usage.volumes_count == 1


def test_get_app_volumes(running_test_app, cleanup):
    """
    Test the test_get_app_volumes function.
    :return: None
    """
    time.sleep(2)  # Wait for the app to start

    # Test with an existing app
    result = get_app_volumes("test_app")

    assert result is not None


def test_get_node_name_by_id():
    """
    Test the get_node_by_id function.
    :return: None
    """

    result = get_node_name_by_id("y07skz469cljq54bm225sohdl")

    assert result == "archlinux"


def test_get_app_service_names(running_test_app, cleanup):
    """
    Test the get_app_service_names function.
    :return: None
    """
    time.sleep(2)  # Wait for the app to start

    # Test with an existing app
    result = get_app_service_names("test_app")

    assert result == ["test_app_busybox", "test_app_nginx"]


def test_get_service_containers_overview(running_test_app, cleanup):
    """
    Test the get_app_containers_overview function.
    :return: None
    """
    time.sleep(2)  # Wait for the app to start

    # Test with an existing service
    result = get_service_containers_overview("test_app_nginx")

    assert isinstance(result, list)
    assert len(result) == 1

    # Test with a non-existing app
    result = get_service_containers_overview("a")

    assert isinstance(result, list)
    assert len(result) == 0

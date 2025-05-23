import pytest
from backend.functions.app.handler import (
    start_app,
    stop_app,
    get_app_state,
    AppState,
    get_apps,
)
from backend.tests.utils import cleanup, create_test_app


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


@pytest.mark.skip
def test_get_app(create_test_app, cleanup):
    """
    Test the get_app function.
    :return: None
    """
    # Test with a non-existing app
    assert get_app_state("non_existing_app") == AppState.UNKNOWN

    # Test with an existing app
    assert get_app_state("test_app") == AppState.STOPPED


def test_get_apps(running_test_app, cleanup):
    """
    Test the get_apps function.
    :return: None
    """

    # Test with no apps
    result = get_apps()
    assert len(result) == 1
    assert result[0].name == "test_app"

from backend.functions.app.handler import start_app, stop_app
from backend.tests.utils import cleanup, create_test_app


def test_start_app(create_test_app, cleanup):
    """
    Test the start_app function.
    :return: None
    """
    # Test with a non-existing app
    assert start_app("non_existing_app") == False

    # Test with an existing app
    assert start_app("test_app") == True


def test_stop_app(create_test_app, cleanup):
    """
    Test the stop_app function.
    :return: None
    """
    # Test with a non-existing app
    assert stop_app("non_existing_app") == False

    # Test with an existing app
    assert stop_app("test_app") == True
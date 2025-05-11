from backend.functions.apps import git_connection


def test_test_connection():
    """
    Test the test_connection function.
    """

    git_url = "https://github.com/gitpython-developers/QuickStartTutorialFiles.git"
    git_folder = "test_folder"
    git_branch = "main"
    git_username = "test_user"
    git_token = "test_token"
    # Test the test_connection function

    git_connection("test",git_url, git_folder, git_branch, git_username, git_token)
    assert True
from fastapi import  APIRouter, HTTPException
from backend.functions import apps
from backend.functions import auth
from backend.functions.apps import write_to_creation_db, get_creation_data
from backend.functions.auth import get_user_by_token

router = APIRouter(prefix="/apps", tags=["apps"])

@router.get("/creation")
async def get_creation(token):
    """
    Gets the saved creation data from the database.
    :param token: The token of the user.
    :return: The app configuration.
    """
    permission_scope = 64

    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    return get_creation_data(get_user_by_token(token))


@router.post("/test_connection")
async def test_connection(token: str,name, git_url: str, git_folder= "/main" , git_branch="main", git_username=None, git_token=None):
    """
    Test connection to the git repository.
    """
    permission_scope = 64
    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    result = apps.git_connection(name=name, git_url=git_url, git_folder=git_folder, git_branch=git_branch,
                                 git_username=git_username, git_token=git_token, editing_user=get_user_by_token(token))

    return result


@router.post("/name_available")
async def name_available(name: str, token: str):
    """
    Check if the name is available.
    :param token:
    :param name: Name to check.
    :return: True if the name is available, False otherwise.
    """
    permission_scope = 64

    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    available = apps.check_name_available(name)
    if available:
        write_to_creation_db(editing_user=get_user_by_token(token), name=name)

    return {"available":available}
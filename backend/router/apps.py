from fastapi import routing, APIRouter, HTTPException
from backend.functions import apps
from backend.functions import auth
router = APIRouter(prefix="/apps", tags=["apps"])

@router.post("/test_connection")
async def test_connection(token: str,name, git_url: str, git_folder= "/" , git_branch="main", git_username=None, git_token=None):
    """
    Test connection to the git repository.
    """
    permission_scope = 64
    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    result = apps.git_connection(git_url, git_folder, git_branch, git_username, git_token)

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

    return {"available":apps.check_name_available(name)}
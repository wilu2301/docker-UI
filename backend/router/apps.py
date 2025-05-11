from fastapi import routing, APIRouter
from backend.functions import apps

router = APIRouter(prefix="/apps", tags=["apps"])

@router.post("/test_connection")
async def test_connection():
    """
    Test connection to the git repository.
    """

    raise NotImplementedError


@router.post("/name_available")
async def name_available(name: str):
    """
    Check if the name is available.
    :param name: Name to check.
    :return: True if the name is available, False otherwise.
    """
    return {"available":apps.check_name_available(name)}
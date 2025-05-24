from fastapi import APIRouter, Depends, HTTPException

from backend.functions.app import apps
from backend.functions.app.models import App
from backend.functions.auth import has_permission

router = APIRouter(prefix="/apps", tags=["apps"])


@router.get("/apps")
def get_apps(token: str) -> list[App]:
    """
    Get all apps from docker.
    :return: list of apps
    """

    if not has_permission(token=token, scope=1):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )

    return apps.get_apps()

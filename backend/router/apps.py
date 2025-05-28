from fastapi import APIRouter, Depends, HTTPException

from backend.functions.app import apps
from backend.functions.app.models import App, AppOverview
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


@router.get("/apps/{app_name}")
def get_app(app_name: str, token: str) -> AppOverview:
    """
    Get an app by name.
    :param app_name: Name of the app.
    :return: App object.
    """

    if not has_permission(token=token, scope=1):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )

    app = apps.get_app(app_name)
    if not app:
        raise HTTPException(status_code=404, detail="App not found.")

    return app


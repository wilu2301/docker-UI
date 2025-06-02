from fastapi import APIRouter, Depends, HTTPException

from backend.functions.app import apps
from backend.functions.app.models import App, AppOverview, Volume
from backend.functions.auth import has_permission

router = APIRouter(prefix="/apps", tags=["apps"])


@router.get("/")
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


@router.get("/{app_name}")
def get_app(app_name: str, token: str) -> AppOverview:
    """
    Get an app by name.
    :param token: Token for authentication.
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


@router.get("/{app_name}/volumes")
def get_volumes(app_name: str, token: str) -> list[Volume]:
    """
    Get the volumes used by the app.
    :param token: Token for authentication.
    :param app_name: Name of the app.
    :return: List of volumes used by the app.
    """

    if not has_permission(token=token, scope=1):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )

    volumes = apps.get_volumes(app_name)
    if not volumes:
        raise HTTPException(status_code=404, detail="No volumes found for this app.")

    return volumes

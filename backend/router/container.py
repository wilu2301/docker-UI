from fastapi import routing, Depends, HTTPException
from backend.functions import docker
from backend.router.auth import has_permission

router = routing.APIRouter(prefix="/containers", tags=["containers"])


@router.get("/all")
async def get_all_containers(token: str):
    """
    Gets all containers on the current client.
    :param token: The token to authenticate the user.
    :return:
    """
    if has_permission(token=token, scope=16):
        return {"containers": docker.get_all_containers()}
    return {"error": "You do not have permission to access this resource."}


@router.get("/get")
def get_container(container_id: str, token: str):
    """
    Gets a container by its id.
    :param container_id: Container name or id.
    :param token: The token to authenticate the user.
    :return:
    """
    if has_permission(token=token, scope=8):
        return {"container": docker.get_container(container_id)}
    return {"error": "You do not have permission to access this resource."}


@router.get("{container_id}/logs")
async def get_container_logs(container_id: str, token: str) -> dict[str, str]:
    """
    Gets the logs of a container.
    :param container_id: The id of the container.
    :param token: The token to authenticate the user.
    :return:
    """
    if not has_permission(token=token, scope=1):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource.",
        )

    return {"logs": docker.get_container_logs(container_id)}

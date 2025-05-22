from fastapi import routing, Depends
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
async def get_container(container_id: str, token: str):
    """
    Gets a container by its id.
    :param container_id: Container name or id.
    :param token: The token to authenticate the user.
    :return:
    """
    if has_permission(token=token, scope=8):
        return {"container": docker.get_container(container_id)}
    return {"error": "You do not have permission to access this resource."}

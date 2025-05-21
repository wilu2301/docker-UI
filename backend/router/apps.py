from fastapi import  APIRouter, HTTPException

import backend.functions.app.setup
from backend.functions.app import apps
from backend.functions import auth
from backend.functions.app.setup import write_to_creation_db, get_creation_data
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


@router.post("/setup_git")
async def test_connection(token: str,name, git_url: str, git_folder= "/main" , git_branch="main", git_username=None, git_token=None):
    """
    Test connection to the git repository.
    """
    permission_scope = 64
    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    result = backend.functions.app.setup.git_connection(name=name, git_url=git_url, git_folder=git_folder, git_branch=git_branch,
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

    available = backend.functions.app.setup.check_name_available(name)
    if available:
        write_to_creation_db(editing_user=get_user_by_token(token), name=name)

    return {"available":available}

@router.post("/setup/claim_port")
async def setup_claim_port(token: str, host_port: int, container_port: int, tcp: bool = True, udp: bool = False):
    """
    Claim a port for the app in setup.
    :param udp: if the port is udp
    :param tcp: if the port is tcp
    :param container_port: the port in the container
    :param host_port: the port on the host
    :param token: The token of the user
    :return: True if the port is available and claimed, False otherwise
    """
    permission_scope = 64

    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    # check if the port is available
    if backend.functions.app.setup.check_port_available(host_port):
        # claim port
        app_id = backend.functions.app.setup.get_app_id_by_token(token)
        if app_id is None:
            raise HTTPException(status_code=400, detail="App does not exist")

        if backend.functions.app.setup.add_port(host_port=host_port, container_port=container_port, tcp=tcp, udp=udp, app_id=app_id, is_setup=True):
            return {"claimed": True}

    return {"claimed": False}

@router.delete("/delete_port")
async def delete_port(token: str, host_port: int):
    """
    Delete a port from the app.
    :param token: The token of the user
    :param host_port: The port to delete
    :return: True if the port is deleted, False otherwise
    """
    permission_scope = 64

    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    app_id = backend.functions.app.setup.get_app_id_by_token(token)
    if app_id is None:
        raise HTTPException(status_code=400, detail="App does not exist")

    if apps.delete_app_port(host_port=host_port, app_id=app_id):
        return {"deleted": True}

    return {"deleted": False}

@router.get("/setup_service")
async def setup_service(token: str, container_name: str, container_image: str):
    """
    Setup a service for the app.
    :param token: The token of the user
    :param container_name: The name of the container
    :param container_image: The image of the container
    :return: True if the service is setup, False otherwise
    """
    permission_scope = 64

    if not auth.has_permission(token, permission_scope):
        raise HTTPException(status_code=403, detail="Permission denied")

    app_id = backend.functions.app.setup.get_app_id_by_token(token)
    if app_id is None:
        raise HTTPException(status_code=400, detail="App does not exist")

    if apps.create_service(app_id=app_id, container_name=container_name, container_image=container_image):
        return {"setup": True}

    return {"setup": False}
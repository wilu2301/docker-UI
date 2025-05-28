from sqlalchemy import Select
from sqlmodel import Session, select

from backend.db.engine import engine
from backend.db.models import Ports, Apps, ServicesSetup
from backend.functions.app import handler
from backend.functions.app import models as md
from backend.functions.app.setup import check_port_available


# section: Services
def create_service(app_id: int, container_name: str, container_image: str) -> bool:
    """
    Create a service for the app.
    :param app_id: App id.
    :param container_name: Container name.
    :param container_image: Container image.
    :return: True if the service was created successfully, False otherwise.
    """

    with Session(engine) as session:
        # Create the service
        service = ServicesSetup(
            app_id=app_id,
            container_name=container_name,
            container_image=container_image,
        )
        session.add(service)
        session.commit()
        return True


# endsection: Services


# section: Ports
def get_app_ports(app_id: int) -> list:
    """
    Get the ports of an app.
    :param app_id: App id.
    :return: List of ports.
    """

    with Session(engine) as session:
        statement: Select = select(Ports).where(Ports.app_id == app_id)
        result = session.exec(statement).all()
        print(result)
        return [port.model_dump() for port in result]


def delete_app_port(host_port: int, app_id: int) -> bool:
    """
    Delete a port from the database.
    :param app_id: The port the app is using.
    :param host_port: Host port to delete.
    :return: success
    """

    with Session(engine) as session:
        # Check if the port exists
        statement: Select = select(Ports).where(
            Ports.host_port == host_port, Ports.app_id == app_id
        )
        result = session.exec(statement).one_or_none()
        if result is None:
            return False

        # Delete the port from the database
        session.delete(result)
        session.commit()
        return True


def add_app_port(
    app_id: int,
    container_port: int,
    host_port: int,
    tcp: bool = False,
    udp: bool = False,
    is_setup=False,
) -> bool:
    """
    Add a port to the database.
    :param app_id: App id.
    :param container_port: Container port.
    :param host_port: Host port.
    :param tcp: If the port uses TCP.
    :param udp: If the port uses UDP.
    :param is_setup: If the app is in setup mode.
    :return: True if the port was added successfully, False otherwise.
    """

    with Session(engine) as session:
        # Check if the port is available
        if not check_port_available(host_port):
            return False

        # Add the port to the database
        port = Ports(
            app_id=app_id,
            container_port=container_port,
            host_port=host_port,
            tcp=tcp,
            udp=udp,
            is_setup=is_setup,
        )
        session.add(port)
        session.commit()
        return True


# endsection: Ports


def get_apps() -> list[md.App]:
    """
    Get all apps from the database.
    :return: List of apps.
    """

    apps: list[md.App] = []

    for app in handler.get_apps():
        if app is None:
            continue
        apps.append(md.App(name=app.name))

    return apps


def get_app(app_name: str) -> md.AppOverview | None:
    """
    Get the app by its id.
    :param app_name: Name of the app.
    :return: App object.
    """

    # Check if the app exists in the database
    with Session(engine) as session:
        statement: Select = select(Apps).where(Apps.name == app_name)
        result = session.exec(statement).one_or_none()
        if result is None:
            return None

    state: md.AppStatus = handler.get_app_state(app_name)
    usage: md.AppUsage | None = handler.get_app_usage(app_name)

    return md.AppOverview(name=app_name, status=state, usage=usage)


def get_app_overview(app_name: str) -> md.AppOverview | None:
    """
    Get the Overview of the app by its name.
    :param app_name: Name of the app.
    :return: App usage object.
    """

    # Check if the app exists in the database
    with Session(engine) as session:
        statement: Select = select(Apps).where(Apps.name == app_name)
        result = session.exec(statement).one_or_none()
        if result is None:
            return None

    overview = handler.get_app_usage(app_name)
    if not usage:
        return None

    return usage
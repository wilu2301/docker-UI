from sqlalchemy import Select
from sqlmodel import Session, select

from backend.db.engine import engine
from backend.db.models import Ports, ServicesSetup


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
        statement: Select = select(Ports).where(Ports.host_port == host_port, Ports.app_id == app_id)
        result = session.exec(statement).one_or_none()
        if result is None:
            return False

        # Delete the port from the database
        session.delete(result)
        session.commit()
        return True


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
        service = ServicesSetup(app_id=app_id, container_name=container_name, container_image=container_image)
        session.add(service)
        session.commit()
        return True


def create_app():
    """
    Creates the App.
    :return:
    """
    return True
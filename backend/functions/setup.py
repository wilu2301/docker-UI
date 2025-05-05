from backend.db.engine import engine
from backend.db.models import User


def setup_database() -> None:
    """
    Creates a default user
    :return: None
    """

    user = User(
        username="admin",
        password="<PASSWORD>",
    )

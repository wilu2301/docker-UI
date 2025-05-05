
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
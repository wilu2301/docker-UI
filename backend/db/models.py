
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)

class Token(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    token: str = Field(nullable=False, unique=True)
    user_id: int | None = Field(nullable=False,unique=True)
    ttl: int = Field(nullable=False)
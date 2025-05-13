
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    username: str = Field(nullable=False,unique=True)
    password: str = Field(nullable=False)
    scope: int = Field(nullable=False) # A binary number representing the users permission level.


class Token(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    token: str = Field(nullable=False, unique=True)
    user_id: int | None = Field(nullable=False,unique=True)
    ttl: int = Field(nullable=False)

class Apps(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(nullable=False, unique=True)
    git: bool = Field(nullable=False, default=False)
    # Git repository url
    git_url: str | None = Field(nullable=True)
    git_branch: str | None = Field(nullable=True)
    git_username: str | None = Field(nullable=True)
    git_token: str | None = Field(nullable=True)
    git_folder: str | None = Field(nullable=True)
    # state

class AppSetup(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    creation_time: int | None = Field(nullable=False)
    editing_user_id: int | None = Field(nullable=False)
    name: str = Field(nullable=True)
    git: bool = Field(nullable=False, default=False)
    # Git repository url
    git_url: str | None = Field(nullable=True)
    git_branch: str | None = Field(nullable=True)
    git_username: str | None = Field(nullable=True)
    git_token: str | None = Field(nullable=True)
    git_folder: str | None = Field(nullable=True)

import enum

from pydantic import BaseModel


class App(BaseModel):
    name: str


class AppStatus(enum.StrEnum):
    RUNNING = "running"
    STOPPED = "stopped"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class AppOverview(BaseModel):
    name: str
    status: AppStatus
    cpu_usage: int = 0
    memory_usage: float = 0.0
    containers_running: int = 0
    ports_exposed: list[int] = []
    volumes_count: int = 0

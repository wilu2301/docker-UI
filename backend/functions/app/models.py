import enum
from datetime import datetime

from pydantic import BaseModel


class App(BaseModel):
    name: str


class AppStatus(enum.StrEnum):
    RUNNING = "running"
    STOPPED = "stopped"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class ContainerStatus(enum.StrEnum):
    CREATED = "created"
    RUNNING = "running"
    RESTARTING = "restarting"
    EXITED = "exited"
    PAUSED = "paused"
    DEAD = "dead"


class Volume(BaseModel):
    name: str
    mountpoint: str
    created_at: datetime
    driver: str


class Port(BaseModel):
    public_port: int
    container_port: int | None = None
    tcp: bool = True
    udp: bool = False
    ingress: bool = False


class AppUsage(BaseModel):
    cpu_usage: int = 0
    memory_usage: float = 0.0
    containers_running: int = 0
    ports_exposed: list[Port]
    volumes_count: int = 0


class AppOverview(BaseModel):
    name: str
    status: AppStatus
    usage: AppUsage | None = None


class ContainerOverview(BaseModel):
    name: str
    image: str
    status: ContainerStatus
    node: str


class AppConfig(BaseModel):
    git: bool = False




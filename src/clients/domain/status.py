from enum import Enum, unique


@unique
class Status(Enum):
    active = "active"
    archived = "archived"

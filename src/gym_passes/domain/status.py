from enum import Enum, unique


@unique
class Status(Enum):
    activated = "activated"
    paused = "paused"
    disabled = "disabled"

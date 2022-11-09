from dataclasses import dataclass
from datetime import datetime

from src.gym_passes.domain.errors import PausingError


@dataclass(frozen=True)
class Pause:
    paused_at: datetime
    days: int

    def __post_init__(self) -> None:
        if self.days > 45:
            raise PausingError("Can not pause gym pass for more than 45 days")

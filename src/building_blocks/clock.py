from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    @abstractmethod
    def get_current_date(self) -> datetime:
        pass

    @staticmethod
    def system_clock() -> "Clock":
        return SystemClock()

    @staticmethod
    def fixed_clock(date: datetime) -> "Clock":
        return FixedClock(date)


class SystemClock(Clock):
    def get_current_date(self) -> datetime:
        return datetime.utcnow()


class FixedClock(Clock):
    def __init__(self, date: datetime) -> None:
        self._date = date

    def get_current_date(self) -> datetime:
        return self._date

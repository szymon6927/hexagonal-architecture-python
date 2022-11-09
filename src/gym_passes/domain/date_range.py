from dataclasses import dataclass
from datetime import datetime

from dateutil.relativedelta import relativedelta

from src.building_blocks.clock import Clock


@dataclass(frozen=True)
class DateRange:
    start_date: datetime
    end_date: datetime

    @classmethod
    def one_month(cls, clock: Clock) -> "DateRange":
        start_date = clock.get_current_date()
        end_date = start_date + relativedelta(months=1)
        return cls(start_date, end_date)

    @classmethod
    def one_year(cls, clock: Clock) -> "DateRange":
        start_date = clock.get_current_date()
        end_date = start_date + relativedelta(years=1)
        return cls(start_date, end_date)

    def is_within_range(self, date: datetime) -> bool:
        return self.start_date <= date <= self.end_date

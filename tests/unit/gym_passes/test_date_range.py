from datetime import datetime, timedelta

from src.building_blocks.clock import Clock
from src.gym_passes.domain.date_range import DateRange


def test_can_change_if_date_is_with_in_range() -> None:
    # given
    clock = Clock.fixed_clock(datetime.now())
    one_month = DateRange.one_month(clock)
    one_year = DateRange.one_year(clock)

    # expect
    assert not one_month.is_within_range(clock.get_current_date() + timedelta(days=50))
    assert one_month.is_within_range(clock.get_current_date() + timedelta(days=12))
    assert not one_year.is_within_range(clock.get_current_date() + timedelta(days=520))
    assert one_year.is_within_range(clock.get_current_date() + timedelta(days=50))

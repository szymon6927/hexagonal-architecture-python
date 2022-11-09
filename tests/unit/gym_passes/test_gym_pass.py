from datetime import datetime, timedelta

import pytest

from src.building_blocks.clock import Clock
from src.gym_passes.domain.date_range import DateRange
from src.gym_passes.domain.errors import GymPassError
from src.gym_passes.domain.gym_pass import GymPass
from src.gym_passes.domain.gym_pass_id import GymPassId
from src.gym_passes.domain.pause import Pause
from src.gym_passes.domain.status import Status


def test_can_create_gym_pass() -> None:
    # when
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)

    # then
    assert gym_pass.active is True
    assert gym_pass.is_owned_by("1234")


def test_can_disable_gym_pass() -> None:
    # when
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)

    # when
    gym_pass.disable()

    # then
    assert gym_pass.active is False


def test_can_activate_gym_pass() -> None:
    # when
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass(GymPassId.new_one(), "1234", Status.disabled, DateRange.one_month(clock), clock, None)

    # when
    gym_pass.activate()

    # then
    assert gym_pass.active is True


def test_can_pause_gym_pass() -> None:
    # given
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)

    # when
    gym_pass.pause(Pause(paused_at=clock.get_current_date(), days=7))

    # then
    assert gym_pass.active is False


def test_can_renew_paused_gym_pass() -> None:
    # given
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass.create_for("1234", DateRange.one_month(clock), clock)

    # when
    gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=10), days=7))

    # and
    gym_pass.renew()

    # then
    assert gym_pass.active is True


def test_can_paused_gym_pass_multiple_times() -> None:
    # given
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass.create_for("1234", DateRange.one_month(clock), clock)

    # when
    gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=10), days=7))
    gym_pass.renew()

    # and
    gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=15), days=7))
    gym_pass.renew()

    # then
    assert gym_pass.active is True


def test_can_not_exceed_maximum_pause_limit() -> None:
    # given
    clock = Clock.fixed_clock(datetime.now())
    gym_pass = GymPass.create_for("1234", DateRange.one_month(clock), clock)

    # when
    gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=10), days=7))
    gym_pass.renew()

    # and
    gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=15), days=7))
    gym_pass.renew()

    # and
    gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=25), days=7))
    gym_pass.renew()

    # then
    with pytest.raises(GymPassError):
        gym_pass.pause(Pause(paused_at=clock.get_current_date() + timedelta(days=45), days=7))

from datetime import datetime

import pytest
from pymongo.database import Database

from src.building_blocks.clock import Clock
from src.gym_passes.domain.date_range import DateRange
from src.gym_passes.domain.errors import GymPassNotFound
from src.gym_passes.domain.gym_pass import GymPass
from src.gym_passes.domain.gym_pass_id import GymPassId
from src.gym_passes.domain.pause import Pause
from src.gym_passes.infrastructure.mongo_gym_pass_repository import MongoDBGymPassRepository


def test_can_get_gym_pass(mongodb: Database) -> None:
    # given
    repository = MongoDBGymPassRepository(mongodb)
    clock = Clock.fixed_clock(datetime(year=2022, month=10, day=27))
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)
    repository.save(gym_pass)

    # when
    fetched_gym_pass = repository.get(gym_pass.id)

    # then
    assert isinstance(fetched_gym_pass, GymPass)
    assert fetched_gym_pass.to_snapshot() == gym_pass.to_snapshot()


def test_should_raise_an_error_if_gym_pass_not_found(mongodb: Database) -> None:
    # given
    repository = MongoDBGymPassRepository(mongodb)

    # expect
    with pytest.raises(GymPassNotFound):
        repository.get(GymPassId.new_one())


def test_can_save_gym_pass(mongodb: Database) -> None:
    # given
    repository = MongoDBGymPassRepository(mongodb)
    clock = Clock.fixed_clock(datetime(year=2022, month=10, day=27))
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)
    repository.save(gym_pass)

    # when
    gym_pass.disable()

    # and
    repository.save(gym_pass)

    # then
    fetched_gym_pass = repository.get(gym_pass.id)
    assert fetched_gym_pass.to_snapshot() == gym_pass.to_snapshot()


def test_can_save_paused_gym_pass(mongodb: Database) -> None:
    # given
    repository = MongoDBGymPassRepository(mongodb)
    clock = Clock.fixed_clock(datetime(year=2022, month=10, day=27))
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)
    repository.save(gym_pass)

    # when
    gym_pass.pause(Pause(paused_at=clock.get_current_date(), days=7))

    # and
    repository.save(gym_pass)

    # then
    fetched_gym_pass = repository.get(gym_pass.id)
    assert fetched_gym_pass.to_snapshot() == gym_pass.to_snapshot()


def test_can_get_gym_pass_by_owner_id(mongodb: Database) -> None:
    # given
    repository = MongoDBGymPassRepository(mongodb)
    clock = Clock.fixed_clock(datetime(year=2022, month=10, day=27))
    gym_pass = GymPass.create_for("1234", DateRange.one_year(clock), clock)
    repository.save(gym_pass)

    # when
    fetched_gym_pass = repository.get_by("1234")

    # then
    assert isinstance(fetched_gym_pass, GymPass)
    assert fetched_gym_pass.to_snapshot() == gym_pass.to_snapshot()

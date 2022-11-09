from datetime import datetime

import pytest

from src.building_blocks.clock import Clock
from src.gym_passes.application.gym_pass_service import GymPassService
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository
from src.gym_passes.infrastructure.in_memory_gym_pass_repository import InMemoryGymPassRepository


@pytest.fixture()
def gym_pass_repo() -> IGymPassRepository:
    return InMemoryGymPassRepository()


@pytest.fixture()
def fixed_clock() -> Clock:
    return Clock.fixed_clock(datetime.now())


@pytest.fixture()
def gym_pass_service(gym_pass_repo: IGymPassRepository, fixed_clock: Clock) -> GymPassService:
    return GymPassService(gym_pass_repo, fixed_clock)

from kink import di

from src.building_blocks.clock import Clock
from src.building_blocks.db import get_mongo_database
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository
from src.gym_passes.facade import GymPassFacade
from src.gym_passes.infrastructure.mongo_gym_pass_repository import MongoDBGymPassRepository
from src.gym_passes.application.gym_pass_service import GymPassService


def bootstrap_di() -> None:
    repository = MongoDBGymPassRepository(get_mongo_database())
    di[IGymPassRepository] = repository
    di[GymPassService] = GymPassService(repository, Clock.system_clock())
    di[GymPassFacade] = GymPassFacade(repository)

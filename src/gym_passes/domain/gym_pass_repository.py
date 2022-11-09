from abc import ABC, abstractmethod

from src.gym_passes.domain.gym_pass import GymPass, OwnerId
from src.gym_passes.domain.gym_pass_id import GymPassId


class IGymPassRepository(ABC):
    @abstractmethod
    def get(self, gym_pass_id: GymPassId) -> GymPass:
        pass

    @abstractmethod
    def get_by(self, owner_id: OwnerId) -> GymPass:
        pass

    @abstractmethod
    def save(self, gym_pass: GymPass) -> None:
        pass

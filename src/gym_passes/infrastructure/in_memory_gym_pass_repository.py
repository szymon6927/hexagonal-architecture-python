import copy

from src.gym_passes.domain.errors import GymPassNotFound
from src.gym_passes.domain.gym_pass import GymPass, OwnerId
from src.gym_passes.domain.gym_pass_id import GymPassId
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository


class InMemoryGymPassRepository(IGymPassRepository):
    def __init__(self) -> None:
        self._gym_passes: dict[GymPassId, GymPass] = {}

    def get(self, gym_pass_id: GymPassId) -> GymPass:
        try:
            return copy.deepcopy(self._gym_passes[gym_pass_id])
        except KeyError as error:
            raise GymPassNotFound(f"Gym pass with id={gym_pass_id} was not found!") from error

    def get_by(self, owner_id: OwnerId) -> GymPass:
        for gym_pass in self._gym_passes.values():
            if gym_pass.is_owned_by(owner_id):
                return copy.deepcopy(gym_pass)

        raise GymPassNotFound(f"Gym pass with owner_id={owner_id} was not found!")

    def save(self, gym_pass: GymPass) -> None:
        self._gym_passes[gym_pass.id] = copy.deepcopy(gym_pass)

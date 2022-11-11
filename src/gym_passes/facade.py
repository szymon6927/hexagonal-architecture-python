from kink import inject

from src.gym_passes.domain.errors import GymPassNotFound
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository


@inject
class GymPassFacade:
    def __init__(self, gym_pass_repo: IGymPassRepository) -> None:
        self._gym_pass_repo = gym_pass_repo

    def disable_for(self, owner_id: str) -> None:
        try:
            gym_pass = self._gym_pass_repo.get_by(owner_id)
            gym_pass.disable()
            self._gym_pass_repo.save(gym_pass)
        except GymPassNotFound:
            return

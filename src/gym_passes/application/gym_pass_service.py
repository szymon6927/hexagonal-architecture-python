from kink import inject

from src.building_blocks.clock import Clock
from src.gym_passes.application.dto import CreateGymPassDTO, GymPassDTO, PauseGymPassDTO
from src.gym_passes.domain.date_range import DateRange
from src.gym_passes.domain.errors import PausingError
from src.gym_passes.domain.gym_pass import GymPass
from src.gym_passes.domain.gym_pass_id import GymPassId
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository
from src.gym_passes.domain.pause import Pause


@inject
class GymPassService:
    def __init__(self, gym_pass_repo: IGymPassRepository, clock: Clock = Clock.system_clock()) -> None:
        self._gym_pass_repo = gym_pass_repo
        self._clock = clock

    def create(self, input_dto: CreateGymPassDTO) -> GymPassDTO:
        period_of_validity = (
            DateRange.one_month(self._clock) if input_dto.validity.ONE_MONTH else DateRange.one_year(self._clock)
        )
        gym_pass = GymPass.create_for(input_dto.owner, period_of_validity, self._clock)

        self._gym_pass_repo.save(gym_pass)

        return GymPassDTO(id=str(gym_pass.id), is_active=gym_pass.active)

    def pause(self, input_dto: PauseGymPassDTO) -> GymPassDTO:
        if not input_dto.gym_pass_id:
            raise PausingError("Gym pass id not provided!")

        gym_pass = self._gym_pass_repo.get(GymPassId.of(input_dto.gym_pass_id))
        gym_pass.pause(Pause(self._clock.get_current_date(), input_dto.days))

        self._gym_pass_repo.save(gym_pass)

        return GymPassDTO(id=str(gym_pass.id), is_active=gym_pass.active)

    def renew(self, gym_pass_id: str) -> GymPassDTO:
        gym_pass = self._gym_pass_repo.get(GymPassId.of(gym_pass_id))
        gym_pass.renew()

        self._gym_pass_repo.save(gym_pass)

        return GymPassDTO(id=str(gym_pass.id), is_active=gym_pass.active)

    def check(self, gym_pass_id: str) -> GymPassDTO:
        gym_pass = self._gym_pass_repo.get(GymPassId.of(gym_pass_id))

        return GymPassDTO(id=str(gym_pass.id), is_active=gym_pass.active)

from src.building_blocks.clock import Clock
from src.gym_passes.application.dto import CreateGymPassDTO, PauseGymPassDTO
from src.gym_passes.application.gym_pass_service import GymPassService
from src.gym_passes.domain.date_range import DateRange
from src.gym_passes.domain.gym_pass import GymPass
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository


def test_can_create_gym_pass(gym_pass_service: GymPassService) -> None:
    # when
    result = gym_pass_service.create(CreateGymPassDTO(owner="123456789", validity=CreateGymPassDTO.Validity.ONE_MONTH))

    # then
    assert result.is_active


def test_can_pause_gym_pass(
    gym_pass_service: GymPassService, gym_pass_repo: IGymPassRepository, fixed_clock: Clock
) -> None:
    # given
    gym_pass = GymPass.create_for("123456789", DateRange.one_month(fixed_clock), fixed_clock)
    gym_pass_repo.save(gym_pass)

    # when
    result = gym_pass_service.pause(PauseGymPassDTO(gym_pass_id=str(gym_pass.id), days=14))

    # then
    assert not result.is_active


def test_can_renew_gym_pass(
    gym_pass_service: GymPassService, gym_pass_repo: IGymPassRepository, fixed_clock: Clock
) -> None:
    # given
    gym_pass = GymPass.create_for("123456789", DateRange.one_month(fixed_clock), fixed_clock)
    gym_pass_repo.save(gym_pass)
    gym_pass_service.pause(PauseGymPassDTO(gym_pass_id=str(gym_pass.id), days=14))
    gym_pass = gym_pass_repo.get(gym_pass.id)

    # when
    result = gym_pass_service.renew(str(gym_pass.id))

    # then
    assert result.is_active

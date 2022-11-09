import pytest
from bson import ObjectId

from src.gym_passes.domain.errors import GymPassError
from src.gym_passes.domain.gym_pass_id import GymPassId


def test_can_create_new_gym_pass_id() -> None:
    # expect
    assert isinstance(GymPassId.new_one(), GymPassId)


def test_can_create_gym_pass_id_from_valid_str() -> None:
    # given
    gym_pass_id = GymPassId.of("6350053dc1f28686b7d7da2f")

    # expect
    assert gym_pass_id.value == ObjectId("6350053dc1f28686b7d7da2f")


def test_should_raise_an_error_if_invalid_id() -> None:
    # expect
    with pytest.raises(GymPassError):
        GymPassId.of("12345")

from datetime import datetime

import pytest

from src.gym_passes.domain.errors import PausingError
from src.gym_passes.domain.pause import Pause


def test_can_not_create_pause_for_more_than_45_days() -> None:
    # expect
    with pytest.raises(PausingError):
        Pause(paused_at=datetime.now(), days=46)

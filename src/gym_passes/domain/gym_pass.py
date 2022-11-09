from typing import Any

from dateutil.relativedelta import relativedelta

from src.building_blocks.clock import Clock
from src.gym_passes.domain.date_range import DateRange
from src.gym_passes.domain.errors import GymPassError
from src.gym_passes.domain.gym_pass_id import GymPassId
from src.gym_passes.domain.pause import Pause
from src.gym_passes.domain.status import Status

OwnerId = str
GymPassSnapshot = dict[str, Any]


class GymPass:
    def __init__(
        self,
        gym_pass_id: GymPassId,
        owner_id: OwnerId,
        status: Status,
        period_of_validity: DateRange,
        clock: Clock,
        pauses: list[Pause] | None,
    ) -> None:
        self._gym_pass_id = gym_pass_id
        self._owner_id = owner_id
        self._status = status
        self._period_of_validity = period_of_validity
        self._clock = clock
        self._pauses = pauses if pauses else []

    @property
    def id(self) -> GymPassId:
        return self._gym_pass_id

    @classmethod
    def create_for(
        cls, owner_id: OwnerId, period_of_validity: DateRange, clock: Clock = Clock.system_clock()
    ) -> "GymPass":
        return cls(
            gym_pass_id=GymPassId.new_one(),
            owner_id=owner_id,
            status=Status.activated,
            period_of_validity=period_of_validity,
            clock=clock,
            pauses=None,
        )

    def is_owned_by(self, owner_id: OwnerId) -> bool:
        return self._owner_id == owner_id

    def activate(self) -> None:
        self._status = Status.activated

    def disable(self) -> None:
        self._status = Status.disabled

    def pause(self, pause: Pause) -> None:
        if not self.active:
            raise GymPassError("Can not pause not active gym pass!")

        if len(self._pauses) >= 3:
            raise GymPassError("The maximum amount of pauses were exceeded!")

        self._status = Status.paused
        self._pauses.append(pause)
        self._pauses.sort(key=lambda pause_item: pause_item.paused_at)

    def renew(self) -> None:
        if self._status == Status.disabled:
            raise GymPassError("Can not renew disabled gym pass!")

        if self._status == Status.activated:
            raise GymPassError("Can not renew active gym pass!")

        latest_pause = self._pauses[-1]
        self._period_of_validity = DateRange(
            start_date=self._period_of_validity.start_date,
            end_date=self._period_of_validity.end_date + relativedelta(days=latest_pause.days),
        )

        self._status = Status.activated

    @property
    def active(self) -> bool:
        if self._status == Status.disabled:
            return False

        if self._status == Status.paused:
            return False

        return self._period_of_validity.is_within_range(self._clock.get_current_date())

    def to_snapshot(self) -> GymPassSnapshot:
        return {
            "id": self._gym_pass_id.value,
            "owner_id": self._owner_id,
            "status": self._status.value,
            "period_of_validity": {
                "from": self._period_of_validity.start_date,
                "to": self._period_of_validity.end_date,
            },
            "pauses": [{"paused_at": pause.paused_at, "days": pause.days} for pause in self._pauses],
        }

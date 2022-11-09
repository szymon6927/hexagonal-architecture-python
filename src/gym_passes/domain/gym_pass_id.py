from dataclasses import dataclass

from bson.errors import InvalidId
from bson.objectid import ObjectId

from src.gym_passes.domain.errors import GymPassError


@dataclass(frozen=True)
class GymPassId:
    value: ObjectId

    @classmethod
    def new_one(cls) -> "GymPassId":
        return GymPassId(ObjectId())

    @classmethod
    def of(cls, id: str) -> "GymPassId":
        try:
            return cls(ObjectId(id))
        except InvalidId:
            raise GymPassError.invalid_id()

    def __str__(self) -> str:
        return str(self.value)

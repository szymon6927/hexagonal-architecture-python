from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CreateGymPassDTO(BaseModel):
    class Validity(str, Enum):
        ONE_MONTH = "ONE_MONTH"
        ONE_YEAR = "ONE_YEAR"

    owner: str
    validity: Validity


class PauseGymPassDTO(BaseModel):
    gym_pass_id: Optional[str]
    days: int


class GymPassDTO(BaseModel):
    id: str
    is_active: bool

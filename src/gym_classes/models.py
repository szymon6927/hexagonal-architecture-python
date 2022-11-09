from pydantic import BaseModel


class GymClass(BaseModel):
    id: str
    name: str
    day: str
    time: str
    coach: str
    description: str | None

    class Config:
        schema_extra = {
            "example": {
                "id": "63500520c1f28686b7d7da2c",
                "name": "Pilates",
                "day": "Monday",
                "time": "10:30-11:30",
                "coach": "Alex W.",
                "description": "A system of physical exercises invented at the beginning of the 20th century by the German Josef Humbertus Pilates",
            }
        }


class CreateOrUpdateClass(BaseModel):
    name: str
    day: str
    time: str
    coach: str
    description: str | None

    class Config:
        schema_extra = {
            "example": {
                "name": "Pilates",
                "day": "Monday",
                "time": "10:30-11:30",
                "coach": "Alex W.",
                "description": "A system of physical exercises invented at the beginning of the 20th century by the German Josef Humbertus Pilates",
            }
        }

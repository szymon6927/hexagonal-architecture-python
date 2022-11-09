import pytest
from bson import ObjectId
from pymongo.database import Database


@pytest.fixture()
def seed_db(mongodb: Database) -> list[dict[str, str]]:
    documents = [
        {
            "_id": ObjectId("63500520c1f28686b7d7da2c"),
            "name": "Pilates 1",
            "day": "Monday",
            "time": "9:00-10:00",
            "coach": "Alex W.",
            "description": "test 1",
        },
        {
            "_id": ObjectId("6350052ac1f28686b7d7da2d"),
            "name": "Cross fit kids",
            "day": "Monday",
            "time": "8:00-9:00",
            "coach": "Alex W.",
            "description": "test 1",
        },
        {
            "_id": ObjectId("63500534c1f28686b7d7da2e"),
            "name": "Pilates 2",
            "day": "Tuesday",
            "time": "9:00-10:00",
            "coach": "Alex W.",
            "description": "test 2",
        },
        {
            "_id": ObjectId("6350053dc1f28686b7d7da2f"),
            "name": "Kickboxing",
            "day": "Tuesday",
            "time": "10:00-11:00",
            "coach": "Alex W.",
            "description": "",
        },
        {
            "_id": ObjectId("63500544c1f28686b7d7da30"),
            "name": "MMA",
            "day": "Wednesday",
            "time": "10:00-11:00",
            "coach": "Alex W.",
            "description": "",
        },
    ]
    mongodb["gym_classes"].insert_many(documents)

    for document in documents:
        document["id"] = str(document["_id"])
        del document["_id"]

    return documents  # type: ignore

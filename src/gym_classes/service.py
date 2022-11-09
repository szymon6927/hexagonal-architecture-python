from bson.objectid import ObjectId
from pymongo.database import Database

from src.gym_classes.errors import GymClassNotFound
from src.gym_classes.models import CreateOrUpdateClass, GymClass


class GymClassService:
    def __init__(self, database: Database) -> None:
        self._collection = database.get_collection("gym_classes")

    def get(self, gym_class_id: ObjectId) -> GymClass:
        document = self._collection.find_one({"_id": gym_class_id})

        if not document:
            raise GymClassNotFound(f"Gym class with id={gym_class_id} was not found!")

        document["id"] = str(document["_id"])
        return GymClass(**document)

    def get_all(self) -> list[GymClass]:
        gym_classes = []
        documents = self._collection.find({})
        for document in documents:
            document["id"] = str(document["_id"])
            gym_classes.append(GymClass(**document))

        days_order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
            "Saturday": 6,
            "Sunday": 7,
        }

        return sorted(gym_classes, key=lambda x: (days_order.get(x.day), x.time))

    def create(self, gym_class_request: CreateOrUpdateClass) -> GymClass:
        document = gym_class_request.dict()
        result = self._collection.insert_one(document)

        return self.get(result.inserted_id)

    def update(self, gym_class_id: str, gym_class_request: CreateOrUpdateClass) -> GymClass:
        gym_class = self.get(ObjectId(gym_class_id))
        gym_class.name = gym_class_request.name
        gym_class.day = gym_class_request.day
        gym_class.time = gym_class_request.time
        gym_class.coach = gym_class_request.coach
        gym_class.description = gym_class_request.description

        new_values = gym_class.dict()
        del new_values["id"]

        self._collection.update_one({"_id": ObjectId(gym_class_id)}, {"$set": new_values})
        return gym_class

    def delete(self, gym_class_id: str) -> None:
        self._collection.delete_one({"_id": ObjectId(gym_class_id)})

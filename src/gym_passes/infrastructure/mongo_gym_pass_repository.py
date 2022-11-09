from pymongo.database import Database
from pymongo.errors import PyMongoError

from src.building_blocks.clock import Clock
from src.building_blocks.custom_types import MongoDocument
from src.building_blocks.errors import RepositoryError
from src.gym_passes.domain.date_range import DateRange
from src.gym_passes.domain.errors import GymPassNotFound
from src.gym_passes.domain.gym_pass import GymPass, OwnerId
from src.gym_passes.domain.gym_pass_id import GymPassId
from src.gym_passes.domain.gym_pass_repository import IGymPassRepository
from src.gym_passes.domain.pause import Pause
from src.gym_passes.domain.status import Status


class MongoDBGymPassRepository(IGymPassRepository):
    def __init__(self, database: Database):
        self._collection = database.get_collection("gym_passes")

    def _to_entity(self, document: MongoDocument) -> GymPass:
        pauses = [Pause(paused_at=item["paused_at"], days=item["days"]) for item in document["pauses"]]
        return GymPass(
            gym_pass_id=GymPassId(document["_id"]),
            owner_id=document["owner_id"],
            status=Status(document["status"]),
            period_of_validity=DateRange(document["period_of_validity"]["from"], document["period_of_validity"]["to"]),
            clock=Clock.system_clock(),
            pauses=pauses,
        )

    def get(self, gym_pass_id: GymPassId) -> GymPass:
        try:
            document = self._collection.find_one({"_id": gym_pass_id.value})

            if not document:
                raise GymPassNotFound(f"Gym pass with id={gym_pass_id} was not found!")

            return self._to_entity(document)
        except PyMongoError as error:
            raise RepositoryError.get_operation_failed() from error

    def get_by(self, owner_id: OwnerId) -> GymPass:
        try:
            document = self._collection.find_one({"owner_id": owner_id})

            if not document:
                raise GymPassNotFound(f"Gym pass with owner_id={owner_id} was not found!")

            return self._to_entity(document)
        except PyMongoError as error:
            raise RepositoryError.get_operation_failed() from error

    def save(self, gym_pass: GymPass) -> None:
        try:
            snapshot = gym_pass.to_snapshot()
            snapshot["_id"] = snapshot["id"]
            del snapshot["id"]

            self._collection.update_one({"_id": snapshot["_id"]}, {"$set": snapshot}, upsert=True)
        except PyMongoError as error:
            raise RepositoryError.save_operation_failed() from error

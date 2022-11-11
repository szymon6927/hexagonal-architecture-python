from pymongo.database import Database
from pymongo.errors import PyMongoError

from src.building_blocks.custom_types import MongoDocument
from src.building_blocks.errors import RepositoryError
from src.clients.domain.client import Client
from src.clients.domain.client_id import ClientId
from src.clients.domain.client_repository import IClientRepository
from src.clients.domain.email_address import EmailAddress
from src.clients.domain.errors import ClientNotFound
from src.clients.domain.status import Status


class MongoDBClientRepository(IClientRepository):
    def __init__(self, database: Database):
        self._collection = database.get_collection("clients")

    def _to_entity(self, document: MongoDocument) -> Client:
        return Client(
            client_id=ClientId.of(str(document["_id"])),
            first_name=document["first_name"],
            last_name=document["last_name"],
            email=EmailAddress(document["email"]),
            status=Status(document["status"]),
        )

    def get_all(self) -> list[Client]:
        clients = []

        try:
            documents = self._collection.find({})
        except PyMongoError as error:
            raise RepositoryError.get_operation_failed() from error

        for document in documents:
            clients.append(self._to_entity(document))

        return clients

    def get(self, client_id: ClientId) -> Client:
        try:
            document = self._collection.find_one({"_id": client_id.value})

            if not document:
                raise ClientNotFound(f"Client with id={client_id} was not found!")

            return self._to_entity(document)
        except PyMongoError as error:
            raise RepositoryError.get_operation_failed() from error

    def save(self, client: Client) -> None:
        try:
            snapshot = client.to_snapshot()
            snapshot["_id"] = snapshot["id"]
            del snapshot["id"]

            self._collection.update_one({"_id": snapshot["_id"]}, {"$set": snapshot}, upsert=True)
        except PyMongoError as error:
            raise RepositoryError.save_operation_failed() from error

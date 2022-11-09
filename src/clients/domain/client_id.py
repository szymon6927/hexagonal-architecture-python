from dataclasses import dataclass

from bson.errors import InvalidId
from bson.objectid import ObjectId

from src.clients.domain.errors import ClientError


@dataclass(frozen=True)
class ClientId:
    value: ObjectId

    @classmethod
    def new_one(cls) -> "ClientId":
        return cls(ObjectId())

    @classmethod
    def of(cls, id: str) -> "ClientId":
        try:
            return cls(ObjectId(id))
        except InvalidId:
            raise ClientError.invalid_id()

    def __str__(self) -> str:
        return str(self.value)

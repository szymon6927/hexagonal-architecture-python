from typing import Any

from src.clients.domain.client_id import ClientId
from src.clients.domain.email_address import EmailAddress
from src.clients.domain.errors import ClientError
from src.clients.domain.status import Status

ClientSnapshot = dict[str, Any]


class Client:
    def __init__(
        self, client_id: ClientId, first_name: str, last_name: str, email: EmailAddress, status: Status
    ) -> None:
        self._id = client_id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._status = status

    @property
    def id(self) -> ClientId:
        return self._id

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def email(self) -> EmailAddress:
        return self._email

    @classmethod
    def create(cls, first_name: str, last_name: str, email: str) -> "Client":
        return cls(ClientId.new_one(), first_name, last_name, EmailAddress(email), Status.active)

    def change_personal_data(self, new_first_name: str, new_last_name: str) -> None:
        if self._status == Status.archived:
            raise ClientError("Can not modify personal data for archived client!")

        self._first_name = new_first_name
        self._last_name = new_last_name

    def change_email(self, new_email: EmailAddress) -> None:
        if self._status == Status.archived:
            raise ClientError("Can not change email address for archived client!")

        self._email = new_email

    def archive(self) -> None:
        self._status = Status.archived

    def is_active(self) -> bool:
        return self._status == Status.active

    def to_snapshot(self) -> ClientSnapshot:
        return {
            "id": self._id.value,
            "first_name": self._first_name,
            "last_name": self._last_name,
            "email": self._email.value,
            "status": self._status.value,
        }

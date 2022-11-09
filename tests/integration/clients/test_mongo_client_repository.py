import pytest
from pymongo.database import Database

from src.clients.domain.client import Client
from src.clients.domain.client_id import ClientId
from src.clients.domain.email_address import EmailAddress
from src.clients.domain.errors import ClientNotFound
from src.clients.infrastructure.mongo_client_repository import MongoDBClientRepository


def test_can_get_client(mongodb: Database) -> None:
    # given
    repository = MongoDBClientRepository(mongodb)
    client = Client.create("John", "Doe", "test@test.com")
    repository.save(client)

    # when
    fetched_client = repository.get(client.id)

    # then
    assert isinstance(fetched_client, Client)
    assert fetched_client.to_snapshot() == client.to_snapshot()


def test_should_raise_an_error_if_client_not_found(mongodb: Database) -> None:
    # given
    repository = MongoDBClientRepository(mongodb)

    # expect
    with pytest.raises(ClientNotFound):
        repository.get(ClientId.new_one())


def test_can_get_all_clients(mongodb: Database) -> None:
    # given
    repository = MongoDBClientRepository(mongodb)
    for i in range(5):
        repository.save(Client.create(f"John {i}", f"Doe {i}", f"test{i}@test.com"))

    # when
    clients = repository.get_all()

    # then
    assert len(clients) == 5


def test_can_save_client(mongodb: Database) -> None:
    # given
    repository = MongoDBClientRepository(mongodb)
    client = Client.create("John", "Doe", "test@test.com")
    repository.save(client)

    # when
    client.change_email(EmailAddress("newmail@test.com"))

    # and
    repository.save(client)

    # then
    client = repository.get(client.id)
    assert client.email == EmailAddress("newmail@test.com")

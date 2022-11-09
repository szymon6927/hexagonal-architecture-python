from unittest.mock import Mock

from src.clients.application.client_service import ClientService
from src.clients.application.dto import (
    ArchiveClientDTO,
    ChangeClientPersonalDataDTO,
    ClientDTO,
    CreateClientDTO,
    ExportClientsDTO,
)
from src.clients.domain.client import Client
from src.clients.domain.client_repository import IClientRepository


def test_can_create_client(client_service: ClientService) -> None:
    # given
    input_dto = CreateClientDTO(first_name="John", last_name="Doe", email="test@test.com")

    # when
    result = client_service.create(input_dto)

    # then
    assert isinstance(result, ClientDTO)


def test_can_change_personal_data(client_service: ClientService, client_repo: IClientRepository) -> None:
    # given
    client = Client.create("John", "Doe", "test@test.com")

    # when
    client_repo.save(client)

    # and
    result = client_service.change_personal_data(
        ChangeClientPersonalDataDTO(
            client_id=str(client.id.value), first_name="Luis", last_name=client.last_name, email=client.email.value
        )
    )

    # then
    assert isinstance(result, ClientDTO)
    assert result.first_name == "Luis"


def test_can_archive_client(
    client_service: ClientService, client_repo: IClientRepository, gym_pass_facade: Mock
) -> None:
    # given
    client = Client.create("John", "Doe", "test@test.com")

    # when
    client_repo.save(client)

    # and
    client_service.archive(ArchiveClientDTO(client_id=str(client.id)))

    # then
    gym_pass_facade.disable_for.assert_called_once_with(str(client.id))


def test_can_export_clients(
    client_service: ClientService, client_repo: IClientRepository, clients_exporter: Mock
) -> None:
    # given
    client = Client.create("John", "Doe", "test@test.com")

    # when
    client_repo.save(client)

    # and
    client_service.export(ExportClientsDTO(format="CSV"))

    # then
    clients_exporter.export.assert_called_once()

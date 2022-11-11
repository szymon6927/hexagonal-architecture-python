from kink import inject

from src.building_blocks.clock import Clock
from src.clients.application.clients_parser import ParserFactory
from src.clients.application.dto import (
    ArchiveClientDTO,
    ChangeClientPersonalDataDTO,
    ClientDTO,
    CreateClientDTO,
    ExportClientsDTO,
)
from src.clients.domain.client import Client
from src.clients.domain.client_id import ClientId
from src.clients.domain.client_repository import IClientRepository
from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.domain.email_address import EmailAddress
from src.clients.domain.report import Report
from src.gym_passes.facade import GymPassFacade


@inject
class ClientService:
    def __init__(
        self,
        client_repo: IClientRepository,
        gym_pass_facade: GymPassFacade,
        clients_exporter: IClientsExporter,
        clock: Clock = Clock.system_clock(),
    ) -> None:
        self._client_repo = client_repo
        self._gym_pass_facade = gym_pass_facade
        self._clients_exporter = clients_exporter
        self._clock = clock

    def create(self, input_dto: CreateClientDTO) -> ClientDTO:
        client = Client.create(input_dto.first_name, input_dto.last_name, input_dto.email)

        self._client_repo.save(client)

        snapshot = client.to_snapshot()
        snapshot["id"] = str(snapshot["id"])
        return ClientDTO(**snapshot)

    def change_personal_data(self, input_dto: ChangeClientPersonalDataDTO) -> ClientDTO:
        client = self._client_repo.get(ClientId.of(input_dto.client_id))  # type: ignore
        client.change_personal_data(input_dto.first_name, input_dto.last_name)
        client.change_email(EmailAddress(input_dto.email))

        self._client_repo.save(client)

        snapshot = client.to_snapshot()
        snapshot["id"] = str(snapshot["id"])
        return ClientDTO(**snapshot)

    def archive(self, input_dto: ArchiveClientDTO) -> None:
        client = self._client_repo.get(ClientId.of(input_dto.client_id))
        client.archive()

        self._client_repo.save(client)

        self._gym_pass_facade.disable_for(str(client.id.value))

    def export(self, input_dto: ExportClientsDTO) -> None:
        clients = self._client_repo.get_all()
        parser = ParserFactory.build(input_dto.format)

        self._clients_exporter.export(
            Report(file_name=f"clients_report_{self._clock.get_current_date()}", content=parser.parse(clients))
        )

from kink import di

from src.building_blocks.db import get_mongo_database
from src.clients.application.client_service import ClientService
from src.clients.application.exporter_factory import Destination, ExporterFactory
from src.clients.domain.client_repository import IClientRepository
from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.infrastructure.mongo_client_repository import MongoDBClientRepository
from src.gym_passes.facade import GymPassFacade


def bootstrap_di() -> None:
    repository = MongoDBClientRepository(get_mongo_database())
    clients_exporter = ExporterFactory.build(Destination.S3)

    di[IClientRepository] = repository
    di[IClientsExporter] = clients_exporter
    di[ClientService] = ClientService(repository, di[GymPassFacade], clients_exporter)

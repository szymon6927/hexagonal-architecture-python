from datetime import datetime, timezone
from typing import Iterator
from unittest.mock import Mock

import boto3
import pytest
from moto import mock_s3

from src.building_blocks.clock import Clock
from src.building_blocks.custom_types import S3SdkClient
from src.clients.application.client_service import ClientService
from src.clients.domain.client_repository import IClientRepository
from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.infrastructure.in_memory_client_repository import InMemoryClientRepository
from src.gym_passes.facade import GymPassFacade


@pytest.fixture()
def s3_mock() -> Iterator[S3SdkClient]:
    with mock_s3():
        s3_sdk_client = boto3.client("s3")
        s3_sdk_resource = boto3.resource("s3")
        bucket_name = "client_reports"

        s3_sdk_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": "eu-west-1"},
        )

        yield s3_sdk_client

        s3_sdk_resource.Bucket(bucket_name).objects.all().delete()
        s3_sdk_client.delete_bucket(Bucket=bucket_name)


@pytest.fixture()
def gym_pass_facade() -> Mock:
    return Mock(spec_set=GymPassFacade)


@pytest.fixture()
def client_repo() -> IClientRepository:
    return InMemoryClientRepository()


@pytest.fixture()
def clients_exporter() -> Mock:
    return Mock(spec_set=IClientsExporter)


@pytest.fixture()
def client_service(client_repo: IClientRepository, gym_pass_facade: Mock, clients_exporter: Mock) -> ClientService:
    return ClientService(
        client_repo, gym_pass_facade, clients_exporter, Clock.fixed_clock(datetime.now(tz=timezone.utc))
    )

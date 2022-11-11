import os
from enum import Enum, unique

import boto3
from dropbox import Dropbox

from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.infrastructure.dropbox_clients_exporter import DropboxClientsExporter
from src.clients.infrastructure.s3_clients_exporter import S3ClientsExporter


@unique
class Destination(str, Enum):
    S3 = "s3"
    DROPBOX = "dropbox"


class ExporterFactory:
    @staticmethod
    def build(destination: Destination) -> IClientsExporter:
        if destination == Destination.S3:
            endpoint_url = "http://localhost:4566" if os.getenv("ENVIRONMENT") == "dev" else None
            s3_sdk = boto3.client("s3", endpoint_url=endpoint_url)
            bucket_name = os.environ["S3_CLIENTS_BUCKET"]
            return S3ClientsExporter(s3_sdk, bucket_name)

        if destination == Destination.DROPBOX:
            dropbox_access_token = os.environ["DROPBOX_ACCESS_TOKEN"]
            dropbox_client = Dropbox(dropbox_access_token)
            return DropboxClientsExporter(dropbox_client)

        raise ValueError("Can not build importer for provided destination!")

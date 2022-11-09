import os

import boto3
from dropbox import Dropbox

from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.infrastructure.dropbox_clients_exporter import DropboxClientsExporter
from src.clients.infrastructure.s3_clients_exporter import S3ClientsExporter


class ExporterFactory:
    @staticmethod
    def build(destination: str) -> IClientsExporter:
        if destination == "s3":
            s3_sdk = boto3.client("s3", endpoint_url="http://localhost:4566")
            bucket_name = os.environ["S3_CLIENTS_BUCKET"]
            return S3ClientsExporter(s3_sdk, bucket_name)

        if destination == "dropbox":
            dropbox_access_token = os.environ["DROPBOX_ACCESS_TOKEN"]
            dropbox_client = Dropbox(dropbox_access_token)
            return DropboxClientsExporter(dropbox_client)

        raise ValueError("Can not build importer for provided destination!")

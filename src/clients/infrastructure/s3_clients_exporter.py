from botocore.exceptions import ClientError

from src.building_blocks.custom_types import S3SdkClient
from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.domain.errors import ExportError
from src.clients.domain.report import Report


class S3ClientsExporter(IClientsExporter):
    def __init__(self, s3_sdk_client: S3SdkClient, bucket_name: str) -> None:
        self._s3_sdk_client = s3_sdk_client
        self._bucket_name = bucket_name

    def export(self, report: Report) -> None:
        try:
            self._s3_sdk_client.put_object(
                Bucket=self._bucket_name, Key=f"reports/{report.file_name}", Body=report.content.read()
            )
        except ClientError as error:
            raise ExportError("Can not export clients report!") from error

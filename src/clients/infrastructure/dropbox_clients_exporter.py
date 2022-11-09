from dropbox import Dropbox
from dropbox.exceptions import DropboxException

from src.clients.domain.clients_exporter import IClientsExporter
from src.clients.domain.errors import ExportError
from src.clients.domain.report import Report


class DropboxClientsExporter(IClientsExporter):
    def __init__(self, dropbox_client: Dropbox) -> None:
        self._client = dropbox_client

    def export(self, report: Report) -> None:
        try:
            self._client.files_upload(report.content_as_bytes(), report.file_name)
        except DropboxException as error:
            raise ExportError("Can not export clients report!") from error

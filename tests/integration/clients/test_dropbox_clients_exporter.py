from io import StringIO
from unittest.mock import Mock

from dropbox import Dropbox

from src.clients.domain.report import Report
from src.clients.infrastructure.dropbox_clients_exporter import DropboxClientsExporter


def test_can_export_clients_report() -> None:
    # given
    dropbox_client_mock = Mock(spec_set=Dropbox)
    exporter = DropboxClientsExporter(dropbox_client_mock)
    report = Report("test_report.csv", StringIO("first_name, last_name\nJohn, Doe"))

    # when
    exporter.export(report)

    # then
    dropbox_client_mock.files_upload.assert_called_once()

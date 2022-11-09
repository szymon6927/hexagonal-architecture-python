from abc import ABC, abstractmethod

from src.clients.domain.report import Report


class IClientsExporter(ABC):
    @abstractmethod
    def export(self, report: Report) -> None:
        pass

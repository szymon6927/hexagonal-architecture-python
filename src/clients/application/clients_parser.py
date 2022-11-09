import csv
import json
from abc import ABC, abstractmethod
from io import StringIO

from src.clients.domain.client import Client


class IClientsParser(ABC):
    @abstractmethod
    def parse(self, clients: list[Client]) -> StringIO:
        pass


class CSVClientsParser(IClientsParser):
    def parse(self, clients: list[Client]) -> StringIO:
        data = [client.to_snapshot() for client in clients]

        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)

        return output


class JSONClientsParser(IClientsParser):
    def parse(self, clients: list[Client]) -> StringIO:
        data = [client.to_snapshot() for client in clients]
        output = StringIO(json.dumps(data))

        return output


class ParserFactory:
    @staticmethod
    def build(expected_output: str) -> IClientsParser:
        if expected_output == "CSV":
            return CSVClientsParser()

        if expected_output == "JSON":
            return JSONClientsParser()

        raise ValueError("Can not build parser based on provided value!")

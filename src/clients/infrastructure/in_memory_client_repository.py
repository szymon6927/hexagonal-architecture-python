import copy

from src.clients.domain.client import Client
from src.clients.domain.client_id import ClientId
from src.clients.domain.client_repository import IClientRepository
from src.clients.domain.errors import ClientNotFound


class InMemoryClientRepository(IClientRepository):
    def __init__(self) -> None:
        self._clients: dict[ClientId, Client] = {}

    def get(self, client_id: ClientId) -> Client:
        try:
            return copy.deepcopy(self._clients[client_id])
        except KeyError:
            raise ClientNotFound(f"Client with id={client_id} was not found!")

    def get_all(self) -> list[Client]:
        clients = []
        for client in self._clients.values():
            clients.append(copy.deepcopy(client))
        return clients

    def save(self, client: Client) -> None:
        self._clients[client.id] = copy.deepcopy(client)

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from kink import di

from src.clients.application.client_service import ClientService
from src.clients.domain.client import Client
from src.clients.domain.client_repository import IClientRepository


@pytest.fixture()
def setup_di(client_service: ClientService) -> None:
    di[ClientService] = client_service


@pytest.mark.usefixtures("setup_di")
def test_can_create_client(test_client: TestClient) -> None:
    # given
    payload = {"first_name": "John", "last_name": "Done", "email": "test@test.com"}

    # when
    response = test_client.post("/clients", json=payload)

    # then
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["first_name"] == payload["first_name"]
    assert response.json()["last_name"] == payload["last_name"]
    assert response.json()["email"] == payload["email"]
    assert response.json()["status"] == "active"


@pytest.mark.usefixtures("setup_di")
def test_can_change_personal_data(test_client: TestClient, client_repo: IClientRepository) -> None:
    # given
    client = Client.create("John", "Doe", "test@test.com")
    client_repo.save(client)
    payload = {"first_name": client.first_name, "last_name": client.last_name, "email": "test1@test.com"}

    # when
    response = test_client.put(f"/clients/{client.id}", json=payload)

    # then
    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.json()
    assert response.json()["email"] == payload["email"]


@pytest.mark.usefixtures("setup_di")
def test_can_archive_client(test_client: TestClient, client_repo: IClientRepository) -> None:
    # given
    client = Client.create("John", "Doe", "test@test.com")
    client_repo.save(client)

    # when
    response = test_client.delete(f"/clients/{client.id}")

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.usefixtures("setup_di")
def test_can_export_clients(test_client: TestClient, client_repo: IClientRepository) -> None:
    # given
    client = Client.create("John", "Doe", "test@test.com")
    client_repo.save(client)

    # when
    response = test_client.post("/clients/exports", json={"format": "CSV"})

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT

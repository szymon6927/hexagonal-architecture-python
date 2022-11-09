import pytest
from bson.objectid import ObjectId

from src.clients.domain.client_id import ClientId
from src.clients.domain.errors import ClientError


def test_can_create_client_id_from_valid_str() -> None:
    # given
    client_id = ClientId.of("6350053dc1f28686b7d7da2f")

    # expect
    assert client_id.value == ObjectId("6350053dc1f28686b7d7da2f")


def test_should_raise_an_error_if_invalid_id() -> None:
    # expect
    with pytest.raises(ClientError):
        ClientId.of("12345")


def test_can_create_new_client_id() -> None:
    # expect
    assert isinstance(ClientId.new_one(), ClientId)


def test_equality() -> None:
    assert ClientId.of("636521bae447a90afcfad9af") == ClientId.of("636521bae447a90afcfad9af")

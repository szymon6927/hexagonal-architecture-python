from src.clients.domain.client import Client
from src.clients.domain.client_id import ClientId
from src.clients.domain.email_address import EmailAddress


def test_can_change_personal_data() -> None:
    # given
    client = Client.create(first_name="John", last_name="Doe", email="test@test.com")

    # when
    client.change_personal_data("Mark", "New")

    # then
    assert isinstance(client.id, ClientId)
    assert client.is_active()
    assert client.first_name == "Mark"
    assert client.last_name == "New"


def test_can_change_email() -> None:
    # given
    client = Client.create(first_name="John", last_name="Doe", email="test@test.com")

    # when
    new_email_address = EmailAddress("newtest@test.com")
    client.change_email(new_email_address)

    # then
    assert client.email == new_email_address


def test_can_archive() -> None:
    # given
    client = Client.create(first_name="John", last_name="Doe", email="test@test.com")

    # when
    client.archive()

    # then
    assert not client.is_active()

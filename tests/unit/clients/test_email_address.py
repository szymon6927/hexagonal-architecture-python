import pytest

from src.clients.domain.email_address import EmailAddress


@pytest.mark.parametrize(
    "invalid_email_address", ["abc.def@mail.c", "abc.def@mail#archive.com", "abc.def@mail", "abc.def@mail..com"]
)
def test_can_validate_email_address(invalid_email_address: str) -> None:
    with pytest.raises(ValueError):
        EmailAddress(invalid_email_address)

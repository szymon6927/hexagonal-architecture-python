from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email


@dataclass(frozen=True)
class EmailAddress:
    value: str

    def __post_init__(self) -> None:
        try:
            validate_email(self.value)
        except EmailNotValidError:
            raise ValueError(f"{self.value} is not a correct e-mail address!")

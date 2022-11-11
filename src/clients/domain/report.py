from dataclasses import dataclass
from io import StringIO


@dataclass(frozen=True)
class Report:
    file_name: str
    content: StringIO

    def __post_init__(self) -> None:
        if not self.file_name:
            raise ValueError("file_name can not be an empty string!")

    def content_as_bytes(self) -> bytes:
        return bytes(self.content.read(), encoding="utf-8")

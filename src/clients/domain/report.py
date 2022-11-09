from dataclasses import dataclass
from io import StringIO


@dataclass(frozen=True)
class Report:
    file_name: str
    content: StringIO

    def content_as_bytes(self) -> bytes:
        return bytes(self.content.read(), encoding="utf-8")

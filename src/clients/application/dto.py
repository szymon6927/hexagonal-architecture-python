from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr


class CreateClientDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ClientDTO(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    status: str


class ChangeClientPersonalDataDTO(BaseModel):
    client_id: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr


class ArchiveClientDTO(BaseModel):
    client_id: str


class ExportFormat(str, Enum):
    CSV = "CSV"
    JSON = "JSON"


class ExportClientsDTO(BaseModel):
    format: ExportFormat

from src.building_blocks.errors import DomainError


class ClientError(DomainError):
    @classmethod
    def invalid_id(cls) -> "ClientError":
        return cls("Provided id is not correct according to the ObjectId standard!")


class ClientNotFound(DomainError):
    pass


class ExportError(DomainError):
    pass

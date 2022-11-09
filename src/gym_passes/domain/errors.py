from src.building_blocks.errors import DomainError


class GymPassError(DomainError):
    @classmethod
    def invalid_id(cls) -> "GymPassError":
        return cls("Provided id is not correct according to the ObjectId standard!")


class PausingError(DomainError):
    pass


class GymPassNotFound(DomainError):
    pass

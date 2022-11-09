class DomainError(Exception):
    pass


class RepositoryError(DomainError):
    @classmethod
    def save_operation_failed(cls) -> "RepositoryError":
        return cls("An error occurred during saving to the database!")

    @classmethod
    def get_operation_failed(cls) -> "RepositoryError":
        return cls("An error occurred while retrieving the data from the database!")

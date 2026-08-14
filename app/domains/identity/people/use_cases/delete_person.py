from dataclasses import dataclass

from app.domains.identity.people.repositories import (
    PersonRepository,
)


@dataclass(frozen=True)
class DeletePersonCommand:
    code: str


@dataclass(frozen=True)
class DeletePersonResult:
    deleted: bool


class DeletePerson:

    def __init__(
        self,
        repository: PersonRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: DeletePersonCommand,
    ) -> DeletePersonResult:

        deleted = self._repository.delete(
            command.code
        )

        return DeletePersonResult(
            deleted=deleted
        )
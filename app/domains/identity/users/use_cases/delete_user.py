from dataclasses import dataclass

from app.domains.identity.users.repositories import (
    UserRepository,
)


@dataclass(frozen=True)
class DeleteUserCommand:
    username: str


@dataclass(frozen=True)
class DeleteUserResult:
    deleted: bool


class DeleteUser:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: DeleteUserCommand,
    ) -> DeleteUserResult:

        deleted = self._repository.delete(
            command.username
        )

        return DeleteUserResult(
            deleted=deleted
        )
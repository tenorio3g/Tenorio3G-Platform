from dataclasses import dataclass

from app.domains.identity.roles.repositories import (
    RoleRepository,
)


@dataclass(frozen=True)
class DeleteRoleCommand:
    code: str


@dataclass(frozen=True)
class DeleteRoleResult:
    deleted: bool


class DeleteRole:

    def __init__(
        self,
        repository: RoleRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: DeleteRoleCommand,
    ) -> DeleteRoleResult:

        deleted = self._repository.delete(
            command.code
        )

        return DeleteRoleResult(
            deleted=deleted
        )
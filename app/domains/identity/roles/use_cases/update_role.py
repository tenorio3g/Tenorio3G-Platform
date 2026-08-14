from dataclasses import dataclass

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    RoleRepository,
)


@dataclass(frozen=True)
class UpdateRoleCommand:
    code: str
    name: str
    description: str = ""
    is_active: bool = True


@dataclass(frozen=True)
class UpdateRoleResult:
    role: Role


class UpdateRole:

    def __init__(
        self,
        repository: RoleRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: UpdateRoleCommand,
    ) -> UpdateRoleResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            raise ValueError(
                "role not found"
            )

        role = Role(
            code=existing.code,
            name=command.name,
            description=command.description,
            is_active=command.is_active,
        )

        self._repository.save(role)

        return UpdateRoleResult(
            role=role
        )
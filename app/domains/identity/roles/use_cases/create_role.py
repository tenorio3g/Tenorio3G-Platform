from dataclasses import dataclass

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    RoleRepository,
)


@dataclass(frozen=True)
class CreateRoleCommand:
    code: str
    name: str
    description: str = ""
    is_active: bool = True


@dataclass(frozen=True)
class CreateRoleResult:
    role: Role


class CreateRole:

    def __init__(
        self,
        repository: RoleRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: CreateRoleCommand,
    ) -> CreateRoleResult:

        normalized_code = str(
            command.code
        ).strip().upper()

        existing = self._repository.get_by_code(
            normalized_code
        )

        if existing is not None:
            raise ValueError(
                "role already exists"
            )

        role = Role(
            code=normalized_code,
            name=command.name,
            description=command.description,
            is_active=command.is_active,
        )

        self._repository.save(role)

        return CreateRoleResult(
            role=role
        )
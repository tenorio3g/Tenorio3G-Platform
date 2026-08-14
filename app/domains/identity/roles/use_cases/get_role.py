from dataclasses import dataclass

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    RoleRepository,
)


@dataclass(frozen=True)
class GetRoleQuery:
    code: str


@dataclass(frozen=True)
class GetRoleResult:
    role: Role | None


class GetRole:

    def __init__(
        self,
        repository: RoleRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetRoleQuery,
    ) -> GetRoleResult:

        role = self._repository.get_by_code(
            query.code
        )

        return GetRoleResult(
            role=role
        )
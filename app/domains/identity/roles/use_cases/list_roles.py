from dataclasses import dataclass

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    RoleRepository,
)


@dataclass(frozen=True)
class ListRolesResult:
    roles: list[Role]


class ListRoles:

    def __init__(
        self,
        repository: RoleRepository,
    ):
        self._repository = repository

    def execute(
        self,
    ) -> ListRolesResult:

        roles = self._repository.list_all()

        return ListRolesResult(
            roles=roles
        )
from app.domains.identity.roles.entities import (
    Role,
)

from .role_repository import (
    RoleRepository,
)


class InMemoryRoleRepository(
    RoleRepository
):

    def __init__(self) -> None:
        self._roles: dict[str, Role] = {}

    def save(
        self,
        role: Role,
    ) -> Role:

        self._roles[role.code] = role

        return role

    def get_by_code(
        self,
        code: str,
    ) -> Role | None:

        normalized_code = str(
            code
        ).strip().upper()

        return self._roles.get(
            normalized_code
        )

    def list_all(
        self,
    ) -> list[Role]:

        return list(
            self._roles.values()
        )

    def delete(
        self,
        code: str,
    ) -> bool:

        normalized_code = str(
            code
        ).strip().upper()

        if normalized_code not in self._roles:
            return False

        del self._roles[
            normalized_code
        ]

        return True
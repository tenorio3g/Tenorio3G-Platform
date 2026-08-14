from dataclasses import dataclass

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    UserRepository,
)


@dataclass(frozen=True)
class ListUsersResult:
    users: list[User]


class ListUsers:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def execute(
        self,
    ) -> ListUsersResult:

        users = self._repository.list_all()

        return ListUsersResult(
            users=users
        )
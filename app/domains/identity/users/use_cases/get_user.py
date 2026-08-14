from dataclasses import dataclass

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    UserRepository,
)


@dataclass(frozen=True)
class GetUserQuery:
    username: str


@dataclass(frozen=True)
class GetUserResult:
    user: User | None


class GetUser:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetUserQuery,
    ) -> GetUserResult:

        user = self._repository.get_by_username(
            query.username
        )

        return GetUserResult(
            user=user
        )
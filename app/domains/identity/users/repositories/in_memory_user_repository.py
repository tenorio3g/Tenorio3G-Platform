from app.domains.identity.users.entities import (
    User,
)

from .user_repository import (
    UserRepository,
)


class InMemoryUserRepository(
    UserRepository
):

    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def save(
        self,
        user: User,
    ) -> User:

        self._users[
            user.username
        ] = user

        return user

    def get_by_username(
        self,
        username: str,
    ) -> User | None:

        normalized_username = str(
            username
        ).strip().lower()

        return self._users.get(
            normalized_username
        )

    def list_all(
        self,
    ) -> list[User]:

        return list(
            self._users.values()
        )

    def delete(
        self,
        username: str,
    ) -> bool:

        normalized_username = str(
            username
        ).strip().lower()

        if (
            normalized_username
            not in self._users
        ):
            return False

        del self._users[
            normalized_username
        ]

        return True
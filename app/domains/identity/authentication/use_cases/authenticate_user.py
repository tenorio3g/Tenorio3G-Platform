from dataclasses import dataclass

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    UserRepository,
)

from app.domains.identity.users.security import (
    PasswordHasher,
)


@dataclass(frozen=True)
class AuthenticateUserCommand:
    username: str
    password: str


@dataclass(frozen=True)
class AuthenticateUserResult:
    authenticated: bool
    user: User | None = None


class AuthenticateUser:

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def execute(
        self,
        command: AuthenticateUserCommand,
    ) -> AuthenticateUserResult:

        user = (
            self._user_repository
            .get_by_username(
                command.username
            )
        )

        if user is None:
            return AuthenticateUserResult(
                authenticated=False
            )

        if not user.is_active:
            return AuthenticateUserResult(
                authenticated=False
            )

        password_is_valid = (
            self._password_hasher.verify(
                command.password,
                user.password_hash,
            )
        )

        if not password_is_valid:
            return AuthenticateUserResult(
                authenticated=False
            )

        return AuthenticateUserResult(
            authenticated=True,
            user=user,
        )
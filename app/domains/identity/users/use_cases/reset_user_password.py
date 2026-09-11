from dataclasses import dataclass

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    UserRepository,
)


@dataclass(frozen=True)
class ResetUserPasswordCommand:
    username: str
    password_hash: str


@dataclass(frozen=True)
class ResetUserPasswordResult:
    success: bool


class ResetUserPassword:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: ResetUserPasswordCommand,
    ) -> ResetUserPasswordResult:

        user = self._repository.get_by_username(
            command.username
        )

        if user is None:
            return ResetUserPasswordResult(
                success=False
            )

        updated_user = User(
            username=user.username,
            password_hash=command.password_hash,
            person_code=user.person_code,
            role_code=user.role_code,
            is_active=user.is_active,
        )

        self._repository.save(
            updated_user
        )

        return ResetUserPasswordResult(
            success=True
        )

from dataclasses import dataclass

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.identity.roles.repositories import (
    RoleRepository,
)

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    UserRepository,
)


@dataclass(frozen=True)
class CreateUserCommand:
    username: str
    password_hash: str
    person_code: str
    role_code: str
    is_active: bool = True


@dataclass(frozen=True)
class CreateUserResult:
    user: User


class CreateUser:

    def __init__(
        self,
        user_repository: UserRepository,
        person_repository: PersonRepository,
        role_repository: RoleRepository,
    ):
        self._user_repository = user_repository
        self._person_repository = person_repository
        self._role_repository = role_repository

    def execute(
        self,
        command: CreateUserCommand,
    ) -> CreateUserResult:

        existing = (
            self._user_repository
            .get_by_username(
                command.username
            )
        )

        if existing is not None:
            raise ValueError(
                "user already exists"
            )

        person = (
            self._person_repository
            .get_by_code(
                command.person_code
            )
        )

        if person is None:
            raise ValueError(
                "person not found"
            )

        role = (
            self._role_repository
            .get_by_code(
                command.role_code
            )
        )

        if role is None:
            raise ValueError(
                "role not found"
            )

        if not person.is_active:
            raise ValueError(
                "person is inactive"
            )

        if not role.is_active:
            raise ValueError(
                "role is inactive"
            )

        user = User(
            username=command.username,
            password_hash=command.password_hash,
            person_code=person.code,
            role_code=role.code,
            is_active=command.is_active,
        )

        self._user_repository.save(
            user
        )

        return CreateUserResult(
            user=user
        )
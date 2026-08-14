from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.use_cases import (
    DeleteUser,
    DeleteUserCommand,
)


def test_should_delete_user():

    repository = (
        InMemoryUserRepository()
    )

    repository.save(
        User(
            username="angel",
            password_hash="HASH",
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    use_case = DeleteUser(
        repository
    )

    result = use_case.execute(
        DeleteUserCommand(
            username="angel"
        )
    )

    assert result.deleted is True

    assert repository.get_by_username(
        "angel"
    ) is None


def test_should_return_false_when_user_does_not_exist():

    repository = (
        InMemoryUserRepository()
    )

    use_case = DeleteUser(
        repository
    )

    result = use_case.execute(
        DeleteUserCommand(
            username="unknown"
        )
    )

    assert result.deleted is False
from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.use_cases import (
    GetUser,
    GetUserQuery,
)


def test_should_get_user():

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

    use_case = GetUser(
        repository
    )

    result = use_case.execute(
        GetUserQuery(
            username="angel"
        )
    )

    assert result.user is not None
    assert result.user.username == "angel"


def test_should_return_none_when_user_does_not_exist():

    repository = (
        InMemoryUserRepository()
    )

    use_case = GetUser(
        repository
    )

    result = use_case.execute(
        GetUserQuery(
            username="unknown"
        )
    )

    assert result.user is None
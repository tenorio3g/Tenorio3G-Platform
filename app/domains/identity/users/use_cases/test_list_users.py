from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.use_cases import (
    ListUsers,
)


def test_should_list_users():

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

    repository.save(
        User(
            username="daniel",
            password_hash="HASH",
            person_code="TECH-002",
            role_code="TECHNICIAN",
        )
    )

    use_case = ListUsers(
        repository
    )

    result = use_case.execute()

    assert len(result.users) == 2


def test_should_return_empty_list():

    repository = (
        InMemoryUserRepository()
    )

    use_case = ListUsers(
        repository
    )

    result = use_case.execute()

    assert result.users == []
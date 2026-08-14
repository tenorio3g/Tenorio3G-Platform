from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)


def create_user(
    username: str = "angel",
) -> User:

    return User(
        username=username,
        password_hash="HASH-DE-PRUEBA",
        person_code="TECH-001",
        role_code="TECHNICIAN",
    )


def test_should_save_and_get_user():

    repository = InMemoryUserRepository()

    user = create_user()

    repository.save(user)

    persisted = repository.get_by_username(
        "angel"
    )

    assert persisted is not None
    assert persisted.username == "angel"
    assert persisted.person_code == "TECH-001"
    assert persisted.role_code == "TECHNICIAN"


def test_should_get_user_with_normalized_username():

    repository = InMemoryUserRepository()

    repository.save(
        create_user()
    )

    persisted = repository.get_by_username(
        " ANGEL "
    )

    assert persisted is not None
    assert persisted.username == "angel"


def test_should_return_none_when_user_does_not_exist():

    repository = InMemoryUserRepository()

    result = repository.get_by_username(
        "unknown"
    )

    assert result is None


def test_should_list_all_users():

    repository = InMemoryUserRepository()

    repository.save(
        create_user(
            username="angel",
        )
    )

    repository.save(
        create_user(
            username="daniel",
        )
    )

    users = repository.list_all()

    assert len(users) == 2

    assert {
        user.username
        for user in users
    } == {
        "angel",
        "daniel",
    }


def test_should_update_existing_user():

    repository = InMemoryUserRepository()

    user = create_user()

    repository.save(user)

    updated_user = User(
        username="angel",
        password_hash="NUEVO-HASH",
        person_code="TECH-001",
        role_code="SUPERVISOR",
        is_active=False,
    )

    repository.save(
        updated_user
    )

    persisted = repository.get_by_username(
        "angel"
    )

    assert persisted is not None
    assert (
        persisted.password_hash
        == "NUEVO-HASH"
    )
    assert persisted.role_code == "SUPERVISOR"
    assert persisted.is_active is False

    assert len(
        repository.list_all()
    ) == 1


def test_should_delete_user():

    repository = InMemoryUserRepository()

    repository.save(
        create_user()
    )

    deleted = repository.delete(
        " ANGEL "
    )

    assert deleted is True

    assert repository.get_by_username(
        "angel"
    ) is None


def test_delete_should_return_false_when_user_does_not_exist():

    repository = InMemoryUserRepository()

    deleted = repository.delete(
        "unknown"
    )

    assert deleted is False
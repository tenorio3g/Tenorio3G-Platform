import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.models import (
    UserModel,
)

from app.domains.identity.users.repositories import (
    SQLiteUserRepository,
)


@pytest.fixture
def repository(tmp_path):

    database_path = (
        tmp_path / "users_test.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        future=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(
        engine
    )

    repository = SQLiteUserRepository(
        SessionLocal
    )

    yield repository

    Base.metadata.drop_all(
        engine
    )

    engine.dispose()


def create_user(
    username="angel",
):
    return User(
        username=username,
        password_hash="HASH-DE-PRUEBA",
        person_code="TECH-001",
        role_code="TECHNICIAN",
    )


def test_should_save_and_get_user(
    repository,
):
    repository.save(
        create_user()
    )

    user = repository.get_by_username(
        "angel"
    )

    assert user is not None
    assert user.username == "angel"
    assert (
        user.password_hash
        == "HASH-DE-PRUEBA"
    )
    assert user.person_code == "TECH-001"
    assert user.role_code == "TECHNICIAN"
    assert user.is_active is True


def test_should_get_user_with_normalized_username(
    repository,
):
    repository.save(
        create_user()
    )

    user = repository.get_by_username(
        " ANGEL "
    )

    assert user is not None
    assert user.username == "angel"


def test_should_update_existing_user(
    repository,
):
    repository.save(
        create_user()
    )

    updated_user = User(
        username="angel",
        password_hash="NUEVO-HASH",
        person_code="TECH-002",
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

    assert (
        persisted.person_code
        == "TECH-002"
    )

    assert (
        persisted.role_code
        == "SUPERVISOR"
    )

    assert persisted.is_active is False


def test_should_list_users_by_username(
    repository,
):
    repository.save(
        create_user(
            username="daniel",
        )
    )

    repository.save(
        create_user(
            username="angel",
        )
    )

    users = repository.list_all()

    assert [
        user.username
        for user in users
    ] == [
        "angel",
        "daniel",
    ]


def test_should_delete_user(
    repository,
):
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


def test_should_return_false_when_deleting_unknown_user(
    repository,
):
    deleted = repository.delete(
        "unknown"
    )

    assert deleted is False
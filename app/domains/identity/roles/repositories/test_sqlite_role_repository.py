import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.models import (
    RoleModel,
)

from app.domains.identity.roles.repositories import (
    SQLiteRoleRepository,
)


@pytest.fixture
def repository(tmp_path):

    database_path = (
        tmp_path / "roles_test.db"
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

    repository = SQLiteRoleRepository(
        SessionLocal
    )

    yield repository

    Base.metadata.drop_all(
        engine
    )

    engine.dispose()


def create_role(
    code="TECHNICIAN",
    name="Técnico",
):
    return Role(
        code=code,
        name=name,
        description="Rol de prueba",
    )


def test_should_save_and_get_role(
    repository,
):
    repository.save(
        create_role()
    )

    role = repository.get_by_code(
        "TECHNICIAN"
    )

    assert role is not None
    assert role.code == "TECHNICIAN"
    assert role.name == "Técnico"
    assert (
        role.description
        == "Rol de prueba"
    )
    assert role.is_active is True


def test_should_get_role_with_normalized_code(
    repository,
):
    repository.save(
        create_role()
    )

    role = repository.get_by_code(
        " technician "
    )

    assert role is not None
    assert role.code == "TECHNICIAN"


def test_should_update_existing_role(
    repository,
):
    role = create_role()

    repository.save(role)

    role.name = "Técnico Senior"
    role.description = (
        "Rol técnico actualizado"
    )
    role.deactivate()

    repository.save(role)

    persisted = repository.get_by_code(
        "TECHNICIAN"
    )

    assert persisted is not None
    assert (
        persisted.name
        == "Técnico Senior"
    )
    assert (
        persisted.description
        == "Rol técnico actualizado"
    )
    assert persisted.is_active is False


def test_should_list_roles_by_name(
    repository,
):
    repository.save(
        create_role(
            code="SUPERVISOR",
            name="Supervisor",
        )
    )

    repository.save(
        create_role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    roles = repository.list_all()

    assert [
        role.name
        for role in roles
    ] == [
        "Supervisor",
        "Técnico",
    ]


def test_should_delete_role(
    repository,
):
    repository.save(
        create_role()
    )

    deleted = repository.delete(
        " technician "
    )

    assert deleted is True

    assert repository.get_by_code(
        "TECHNICIAN"
    ) is None


def test_should_return_false_when_deleting_unknown_role(
    repository,
):
    deleted = repository.delete(
        "UNKNOWN"
    )

    assert deleted is False
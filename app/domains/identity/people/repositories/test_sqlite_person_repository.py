import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.models import (
    PersonModel,
)

from app.domains.identity.people.repositories import (
    SQLitePersonRepository,
)


@pytest.fixture
def repository(tmp_path):

    database_path = (
        tmp_path / "people_test.db"
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

    Base.metadata.create_all(engine)

    repository = SQLitePersonRepository(
        SessionLocal
    )

    yield repository

    Base.metadata.drop_all(engine)
    engine.dispose()


def create_person(
    code="TECH-001",
    name="Angel",
):
    return Person(
        code=code,
        name=name,
        position="Technician",
    )


def test_should_save_and_get_person(
    repository,
):
    repository.save(
        create_person()
    )

    person = repository.get_by_code(
        "TECH-001"
    )

    assert person is not None
    assert person.code == "TECH-001"
    assert person.name == "Angel"
    assert person.position == "Technician"
    assert person.is_active is True


def test_should_persist_person_between_sessions(
    repository,
):
    repository.save(
        create_person()
    )

    person = repository.get_by_code(
        "TECH-001"
    )

    assert person is not None
    assert person.name == "Angel"


def test_should_update_existing_person(
    repository,
):
    person = create_person()

    repository.save(person)

    person.name = "Angel Updated"
    person.position = "Senior Technician"
    person.deactivate()

    repository.save(person)

    persisted = repository.get_by_code(
        "TECH-001"
    )

    assert persisted is not None
    assert persisted.name == "Angel Updated"
    assert (
        persisted.position
        == "Senior Technician"
    )
    assert persisted.is_active is False


def test_should_list_people_by_name(
    repository,
):
    repository.save(
        create_person(
            code="TECH-002",
            name="Daniel",
        )
    )

    repository.save(
        create_person(
            code="TECH-001",
            name="Angel",
        )
    )

    people = repository.list_all()

    assert [
        person.name
        for person in people
    ] == [
        "Angel",
        "Daniel",
    ]


def test_should_delete_person(
    repository,
):
    repository.save(
        create_person()
    )

    deleted = repository.delete(
        "TECH-001"
    )

    assert deleted is True

    assert repository.get_by_code(
        "TECH-001"
    ) is None


def test_should_return_false_when_deleting_unknown_person(
    repository,
):
    deleted = repository.delete(
        "UNKNOWN"
    )

    assert deleted is False
from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)


def create_person(
    code: str = "TECH-001",
    name: str = "Angel",
) -> Person:

    return Person(
        code=code,
        name=name,
        position="Technician",
    )


def test_should_save_and_get_person() -> None:

    repository = InMemoryPersonRepository()

    person = create_person()

    repository.save(person)

    persisted = repository.get_by_code(
        "TECH-001"
    )

    assert persisted is not None
    assert persisted.code == "TECH-001"
    assert persisted.name == "Angel"


def test_should_return_none_when_person_does_not_exist() -> None:

    repository = InMemoryPersonRepository()

    result = repository.get_by_code(
        "DOES-NOT-EXIST"
    )

    assert result is None


def test_should_list_all_people() -> None:

    repository = InMemoryPersonRepository()

    repository.save(
        create_person(
            code="TECH-001",
            name="Angel",
        )
    )

    repository.save(
        create_person(
            code="TECH-002",
            name="Daniel",
        )
    )

    people = repository.list_all()

    assert len(people) == 2

    assert {
        person.code
        for person in people
    } == {
        "TECH-001",
        "TECH-002",
    }


def test_should_update_existing_person() -> None:

    repository = InMemoryPersonRepository()

    person = create_person()

    repository.save(person)

    person.position = "Senior Technician"

    repository.save(person)

    persisted = repository.get_by_code(
        "TECH-001"
    )

    assert persisted is not None
    assert (
        persisted.position
        == "Senior Technician"
    )

    assert len(repository.list_all()) == 1


def test_should_delete_person() -> None:

    repository = InMemoryPersonRepository()

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


def test_delete_should_return_false_when_person_does_not_exist() -> None:

    repository = InMemoryPersonRepository()

    deleted = repository.delete(
        "DOES-NOT-EXIST"
    )

    assert deleted is False
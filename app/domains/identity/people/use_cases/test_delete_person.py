from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.identity.people.use_cases import (
    DeletePerson,
    DeletePersonCommand,
)


def test_should_delete_person():

    repository = InMemoryPersonRepository()

    repository.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    use_case = DeletePerson(repository)

    result = use_case.execute(
        DeletePersonCommand(
            code="TECH-001"
        )
    )

    assert result.deleted is True

    assert repository.get_by_code(
        "TECH-001"
    ) is None


def test_should_return_false_when_person_does_not_exist():

    repository = InMemoryPersonRepository()

    use_case = DeletePerson(repository)

    result = use_case.execute(
        DeletePersonCommand(
            code="UNKNOWN"
        )
    )

    assert result.deleted is False
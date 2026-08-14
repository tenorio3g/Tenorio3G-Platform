import pytest

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.identity.people.use_cases import (
    CreatePerson,
    CreatePersonCommand,
)


def test_should_create_person():

    repository = InMemoryPersonRepository()

    use_case = CreatePerson(repository)

    result = use_case.execute(
        CreatePersonCommand(
            code="TECH-001",
            name="Angel",
            position="Technician",
        )
    )

    assert result.person.code == "TECH-001"
    assert result.person.name == "Angel"

    persisted = repository.get_by_code(
        "TECH-001"
    )

    assert persisted is not None


def test_should_reject_duplicate_person():

    repository = InMemoryPersonRepository()

    use_case = CreatePerson(repository)

    command = CreatePersonCommand(
        code="TECH-001",
        name="Angel",
    )

    use_case.execute(command)

    with pytest.raises(
        ValueError,
        match="person already exists",
    ):
        use_case.execute(command)
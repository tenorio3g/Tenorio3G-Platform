import pytest

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.identity.people.use_cases import (
    UpdatePerson,
    UpdatePersonCommand,
)


def test_should_update_person():

    repository = InMemoryPersonRepository()

    repository.save(
        Person(
            code="TECH-001",
            name="Angel",
            position="Technician",
        )
    )

    use_case = UpdatePerson(repository)

    result = use_case.execute(
        UpdatePersonCommand(
            code="TECH-001",
            name="Angel Updated",
            position="Senior Technician",
            is_active=False,
        )
    )

    assert result.person.code == "TECH-001"
    assert result.person.name == "Angel Updated"
    assert (
        result.person.position
        == "Senior Technician"
    )
    assert result.person.is_active is False

    persisted = repository.get_by_code(
        "TECH-001"
    )

    assert persisted is not None
    assert persisted.name == "Angel Updated"
    assert persisted.is_active is False


def test_should_reject_unknown_person():

    repository = InMemoryPersonRepository()

    use_case = UpdatePerson(repository)

    with pytest.raises(
        ValueError,
        match="person not found",
    ):
        use_case.execute(
            UpdatePersonCommand(
                code="UNKNOWN",
                name="Unknown",
            )
        )
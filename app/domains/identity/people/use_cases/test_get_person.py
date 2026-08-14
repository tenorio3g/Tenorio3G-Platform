from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.identity.people.use_cases import (
    GetPerson,
    GetPersonQuery,
)


def test_should_get_person():

    repository = InMemoryPersonRepository()

    repository.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    use_case = GetPerson(repository)

    result = use_case.execute(
        GetPersonQuery(
            code="TECH-001"
        )
    )

    assert result.person is not None
    assert result.person.name == "Angel"


def test_should_return_none_when_person_does_not_exist():

    repository = InMemoryPersonRepository()

    use_case = GetPerson(repository)

    result = use_case.execute(
        GetPersonQuery(
            code="UNKNOWN"
        )
    )

    assert result.person is None
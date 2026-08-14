from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.identity.people.use_cases import (
    ListPeople,
)


def test_should_list_people():

    repository = InMemoryPersonRepository()

    repository.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    repository.save(
        Person(
            code="TECH-002",
            name="Daniel",
        )
    )

    use_case = ListPeople(repository)

    result = use_case.execute()

    assert len(result.people) == 2


def test_should_return_empty_list():

    repository = InMemoryPersonRepository()

    use_case = ListPeople(repository)

    result = use_case.execute()

    assert result.people == []
from dataclasses import dataclass

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)


@dataclass(frozen=True)
class ListPeopleResult:
    people: list[Person]


class ListPeople:

    def __init__(
        self,
        repository: PersonRepository,
    ):
        self._repository = repository

    def execute(self) -> ListPeopleResult:

        people = self._repository.list_all()

        return ListPeopleResult(
            people=people
        )
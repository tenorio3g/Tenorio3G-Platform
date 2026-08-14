from dataclasses import dataclass

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)


@dataclass(frozen=True)
class GetPersonQuery:
    code: str


@dataclass(frozen=True)
class GetPersonResult:
    person: Person | None


class GetPerson:

    def __init__(
        self,
        repository: PersonRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetPersonQuery,
    ) -> GetPersonResult:

        person = self._repository.get_by_code(
            query.code
        )

        return GetPersonResult(
            person=person
        )
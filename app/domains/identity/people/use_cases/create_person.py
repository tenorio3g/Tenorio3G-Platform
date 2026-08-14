from dataclasses import dataclass

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)


@dataclass(frozen=True)
class CreatePersonCommand:
    code: str
    name: str
    position: str = ""
    is_active: bool = True


@dataclass(frozen=True)
class CreatePersonResult:
    person: Person


class CreatePerson:

    def __init__(
        self,
        repository: PersonRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: CreatePersonCommand,
    ) -> CreatePersonResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is not None:
            raise ValueError(
                "person already exists"
            )

        person = Person(
            code=command.code,
            name=command.name,
            position=command.position,
            is_active=command.is_active,
        )

        self._repository.save(person)

        return CreatePersonResult(
            person=person
        )
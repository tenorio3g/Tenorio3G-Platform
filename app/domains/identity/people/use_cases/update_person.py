from dataclasses import dataclass

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)


@dataclass(frozen=True)
class UpdatePersonCommand:
    code: str
    name: str
    position: str = ""
    is_active: bool = True


@dataclass(frozen=True)
class UpdatePersonResult:
    person: Person


class UpdatePerson:

    def __init__(
        self,
        repository: PersonRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: UpdatePersonCommand,
    ) -> UpdatePersonResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            raise ValueError(
                "person not found"
            )

        person = Person(
            code=existing.code,
            name=command.name,
            position=command.position,
            is_active=command.is_active,
        )

        self._repository.save(person)

        return UpdatePersonResult(
            person=person
        )
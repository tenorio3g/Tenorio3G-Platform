from app.domains.identity.people.entities import (
    Person,
)

from .person_repository import (
    PersonRepository,
)


class InMemoryPersonRepository(
    PersonRepository
):

    def __init__(self) -> None:
        self._people: dict[str, Person] = {}

    def save(
        self,
        person: Person,
    ) -> Person:

        self._people[person.code] = person

        return person

    def get_by_code(
        self,
        code: str,
    ) -> Person | None:

        return self._people.get(
            str(code).strip()
        )

    def list_all(
        self,
    ) -> list[Person]:

        return list(
            self._people.values()
        )

    def delete(
        self,
        code: str,
    ) -> bool:

        code = str(code).strip()

        if code not in self._people:
            return False

        del self._people[code]

        return True
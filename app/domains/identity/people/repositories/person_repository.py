from abc import ABC, abstractmethod

from app.domains.identity.people.entities import (
    Person,
)


class PersonRepository(ABC):

    @abstractmethod
    def save(
        self,
        person: Person,
    ) -> Person:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> Person | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Person]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> bool:
        raise NotImplementedError
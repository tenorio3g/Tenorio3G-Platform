from abc import ABC, abstractmethod

from app.domains.identity.users.entities import (
    User,
)


class UserRepository(ABC):

    @abstractmethod
    def save(
        self,
        user: User,
    ) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(
        self,
        username: str,
    ) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        username: str,
    ) -> bool:
        raise NotImplementedError
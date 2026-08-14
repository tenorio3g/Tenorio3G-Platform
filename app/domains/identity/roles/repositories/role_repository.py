from abc import ABC, abstractmethod

from app.domains.identity.roles.entities import (
    Role,
)


class RoleRepository(ABC):

    @abstractmethod
    def save(
        self,
        role: Role,
    ) -> Role:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(
        self,
    ) -> list[Role]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> bool:
        raise NotImplementedError
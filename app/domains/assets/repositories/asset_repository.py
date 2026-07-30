from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.domains.assets.entities.asset import Asset


class AssetRepository(ABC):
    """
    Contrato de persistencia para activos físicos.

    Los casos de uso dependen de esta abstracción y no de una
    implementación concreta de base de datos.
    """

    @abstractmethod
    def save(
        self,
        asset: Asset,
    ) -> None:
        """
        Guarda un activo nuevo.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_code(
        self,
        code: str,
    ) -> Asset | None:
        """
        Busca un activo por su código único.
        """
        raise NotImplementedError

    @abstractmethod
    def find_all(
        self,
    ) -> list[Asset]:
        """
        Devuelve todos los activos registrados.
        """
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        asset: Asset,
    ) -> None:
        """
        Persiste los cambios de un activo existente.
        """
        raise NotImplementedError
"""
Contrato del repositorio para los modelos de activos.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.assets.entities.asset_model import AssetModel


class AssetModelRepository(ABC):
    """
    Define las operaciones de persistencia disponibles
    para los modelos de activos.
    """

    @abstractmethod
    def save(self, asset_model: AssetModel) -> None:
        """
        Guarda un modelo de activo.
        """
        raise NotImplementedError

    @abstractmethod
    def exists_by_code(self, code: str) -> bool:
        """
        Indica si existe un modelo con el código recibido.
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_code(self, code: str) -> AssetModel | None:
        """
        Busca un modelo mediante su código.
        """
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[AssetModel]:
        """
        Devuelve todos los modelos registrados.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self, asset_model: AssetModel) -> None:
        """
        Actualiza un modelo existente.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_by_code(self, code: str) -> None:
        """
        Elimina un modelo mediante su código.
        """
        raise NotImplementedError
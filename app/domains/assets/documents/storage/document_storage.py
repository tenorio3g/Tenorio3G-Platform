from abc import ABC, abstractmethod
from pathlib import Path


class DocumentStorage(ABC):
    """
    Contrato para el almacenamiento físico
    de documentos técnicos.
    """

    @abstractmethod
    def save(
        self,
        source_path: Path,
        stored_name: str,
    ) -> Path:
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        stored_name: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_path(
        self,
        stored_name: str,
    ) -> Path:
        raise NotImplementedError
    

    @abstractmethod
    def delete(
        self,
        stored_name: str,
    ) -> None:
        raise NotImplementedError


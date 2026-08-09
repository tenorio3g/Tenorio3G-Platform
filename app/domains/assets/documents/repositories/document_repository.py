from abc import ABC, abstractmethod

from app.domains.assets.documents.entities import Document


class DocumentRepository(ABC):

    @abstractmethod
    def save(self, document: Document) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, code: str) -> Document | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, code: str) -> None:
        raise NotImplementedError


class InMemoryDocumentRepository(DocumentRepository):

    def __init__(self) -> None:
        self._documents: dict[str, Document] = {}

    def save(self, document: Document) -> None:
        self._documents[document.code] = document

    def get_by_code(self, code: str) -> Document | None:
        return self._documents.get(code)

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[Document]:
        return [
            document
            for document in self._documents.values()
            if document.asset_code == asset_code
        ]

    def delete(self, code: str) -> None:
        self._documents.pop(code, None)
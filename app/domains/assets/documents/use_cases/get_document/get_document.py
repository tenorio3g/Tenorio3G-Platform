from dataclasses import dataclass

from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    DocumentRepository,
)


@dataclass
class GetDocumentQuery:
    code: str


@dataclass
class GetDocumentResult:
    document: Document | None


class GetDocument:

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: GetDocumentQuery,
    ) -> GetDocumentResult:

        document = self._repository.get_by_code(
            query.code
        )

        return GetDocumentResult(
            document=document
        )
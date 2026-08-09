from dataclasses import dataclass

from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    DocumentRepository,
)


@dataclass
class ListDocumentsByAssetQuery:
    asset_code: str


@dataclass
class ListDocumentsByAssetResult:
    documents: list[Document]


class ListDocumentsByAsset:

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: ListDocumentsByAssetQuery,
    ) -> ListDocumentsByAssetResult:

        documents = self._repository.get_by_asset_code(
            query.asset_code
        )

        return ListDocumentsByAssetResult(
            documents=documents
        )
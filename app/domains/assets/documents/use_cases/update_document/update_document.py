from dataclasses import dataclass

from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    DocumentRepository,
)


@dataclass
class UpdateDocumentCommand:
    code: str
    asset_code: str
    title: str
    document_type: str
    file_name: str
    description: str = ""
    revision: str = ""


@dataclass
class UpdateDocumentResult:
    success: bool
    document: Document | None


class UpdateDocument:

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: UpdateDocumentCommand,
    ) -> UpdateDocumentResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            return UpdateDocumentResult(
                success=False,
                document=None,
            )

        document = Document(
            code=command.code,
            asset_code=command.asset_code,
            title=command.title,
            document_type=command.document_type,
            file_name=command.file_name,
            description=command.description,
            revision=command.revision,
            created_at=existing.created_at,
        )

        self._repository.save(document)

        return UpdateDocumentResult(
            success=True,
            document=document,
        )
from dataclasses import dataclass

from app.domains.assets.documents.repositories import (
    DocumentRepository,
)


@dataclass
class DeleteDocumentCommand:
    code: str


@dataclass
class DeleteDocumentResult:
    success: bool


class DeleteDocument:

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: DeleteDocumentCommand,
    ) -> DeleteDocumentResult:

        document = self._repository.get_by_code(
            command.code
        )

        if document is None:
            return DeleteDocumentResult(
                success=False
            )

        self._repository.delete(
            command.code
        )

        return DeleteDocumentResult(
            success=True
        )
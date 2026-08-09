from dataclasses import dataclass

from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    DocumentRepository,
)


@dataclass
class CreateDocumentCommand:
    code: str
    asset_code: str
    title: str
    document_type: str
    file_name: str
    description: str = ""
    revision: str = ""


@dataclass
class CreateDocumentResult:
    success: bool
    document: Document


class CreateDocument:

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: CreateDocumentCommand,
    ) -> CreateDocumentResult:

        document = Document(
            code=command.code,
            asset_code=command.asset_code,
            title=command.title,
            document_type=command.document_type,
            file_name=command.file_name,
            description=command.description,
            revision=command.revision,
        )

        self._repository.save(document)

        return CreateDocumentResult(
            success=True,
            document=document,
        )
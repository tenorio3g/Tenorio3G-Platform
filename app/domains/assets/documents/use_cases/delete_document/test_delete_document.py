from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    InMemoryDocumentRepository,
)

from app.domains.assets.documents.use_cases.delete_document import (
    DeleteDocument,
    DeleteDocumentCommand,
)


def test_should_delete_existing_document() -> None:

    repository = InMemoryDocumentRepository()

    repository.save(
        Document(
            code="DOC-ES09-001",
            asset_code="ES09",
            title="Manual",
            document_type="manual",
            file_name="manual.pdf",
        )
    )

    use_case = DeleteDocument(repository)

    result = use_case.execute(
        DeleteDocumentCommand(
            code="DOC-ES09-001"
        )
    )

    assert result.success is True

    assert repository.get_by_code(
        "DOC-ES09-001"
    ) is None


def test_should_not_delete_nonexistent_document() -> None:

    repository = InMemoryDocumentRepository()

    use_case = DeleteDocument(repository)

    result = use_case.execute(
        DeleteDocumentCommand(
            code="DOC-NOT-FOUND"
        )
    )

    assert result.success is False
from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    InMemoryDocumentRepository,
)

from app.domains.assets.documents.use_cases.update_document import (
    UpdateDocument,
    UpdateDocumentCommand,
)


def test_should_update_existing_document() -> None:

    repository = InMemoryDocumentRepository()

    repository.save(
        Document(
            code="DOC-ES09-001",
            asset_code="ES09",
            title="Manual original",
            document_type="manual",
            file_name="manual_original.pdf",
            revision="A",
        )
    )

    original = repository.get_by_code(
        "DOC-ES09-001"
    )

    assert original is not None

    original_created_at = original.created_at

    use_case = UpdateDocument(repository)

    result = use_case.execute(
        UpdateDocumentCommand(
            code="DOC-ES09-001",
            asset_code="ES09",
            title="Manual actualizado",
            document_type="manual",
            file_name="manual_actualizado.pdf",
            description="Nueva revisión.",
            revision="B",
        )
    )

    assert result.success is True
    assert result.document is not None
    assert result.document.title == "Manual actualizado"
    assert result.document.revision == "B"
    assert result.document.created_at == original_created_at

    persisted = repository.get_by_code(
        "DOC-ES09-001"
    )

    assert persisted is not None
    assert persisted.file_name == "manual_actualizado.pdf"


def test_should_not_update_nonexistent_document() -> None:

    repository = InMemoryDocumentRepository()

    use_case = UpdateDocument(repository)

    result = use_case.execute(
        UpdateDocumentCommand(
            code="DOC-NOT-FOUND",
            asset_code="ES09",
            title="Documento",
            document_type="manual",
            file_name="document.pdf",
        )
    )

    assert result.success is False
    assert result.document is None
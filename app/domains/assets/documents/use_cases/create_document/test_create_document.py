from app.domains.assets.documents.repositories import (
    InMemoryDocumentRepository,
)

from app.domains.assets.documents.use_cases.create_document import (
    CreateDocument,
    CreateDocumentCommand,
)


def test_should_create_document() -> None:

    repository = InMemoryDocumentRepository()

    use_case = CreateDocument(
        repository
    )

    result = use_case.execute(
        CreateDocumentCommand(
            code="DOC-ES09-001",
            asset_code="ES09",
            title="Diagrama unifilar ES09",
            document_type="electrical_diagram",
            file_name="ES09_unifilar.pdf",
            description="Diagrama eléctrico.",
            revision="A",
        )
    )

    assert result.success is True

    assert result.document.code == "DOC-ES09-001"
    assert result.document.asset_code == "ES09"
    assert result.document.title == "Diagrama unifilar ES09"
    assert result.document.document_type == "electrical_diagram"
    assert result.document.file_name == "ES09_unifilar.pdf"
    assert result.document.description == "Diagrama eléctrico."
    assert result.document.revision == "A"


def test_should_persist_created_document() -> None:

    repository = InMemoryDocumentRepository()

    use_case = CreateDocument(
        repository
    )

    use_case.execute(
        CreateDocumentCommand(
            code="DOC-ES09-002",
            asset_code="ES09",
            title="Manual ES09",
            document_type="manual",
            file_name="manual_es09.pdf",
        )
    )

    persisted = repository.get_by_code(
        "DOC-ES09-002"
    )

    assert persisted is not None
    assert persisted.code == "DOC-ES09-002"
    assert persisted.asset_code == "ES09"
    assert persisted.title == "Manual ES09"
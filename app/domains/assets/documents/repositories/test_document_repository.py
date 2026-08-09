from app.domains.assets.documents.entities import Document
from app.domains.assets.documents.repositories import (
    InMemoryDocumentRepository,
)


def create_document(
    code: str = "DOC-ES09-001",
    asset_code: str = "ES09",
) -> Document:
    return Document(
        code=code,
        asset_code=asset_code,
        title="Diagrama unifilar",
        document_type="electrical_diagram",
        file_name=f"{code}.pdf",
    )


def test_should_save_and_get_document_by_code() -> None:
    repository = InMemoryDocumentRepository()

    document = create_document()

    repository.save(document)

    result = repository.get_by_code(
        "DOC-ES09-001"
    )

    assert result is document


def test_should_return_none_when_document_does_not_exist() -> None:
    repository = InMemoryDocumentRepository()

    result = repository.get_by_code(
        "DOC-NOT-FOUND"
    )

    assert result is None


def test_should_get_documents_by_asset_code() -> None:
    repository = InMemoryDocumentRepository()

    repository.save(
        create_document(
            code="DOC-ES09-001",
            asset_code="ES09",
        )
    )

    repository.save(
        create_document(
            code="DOC-ES09-002",
            asset_code="ES09",
        )
    )

    repository.save(
        create_document(
            code="DOC-CH11-001",
            asset_code="CH11",
        )
    )

    documents = repository.get_by_asset_code(
        "ES09"
    )

    assert len(documents) == 2

    assert all(
        document.asset_code == "ES09"
        for document in documents
    )


def test_should_delete_document() -> None:
    repository = InMemoryDocumentRepository()

    repository.save(
        create_document()
    )

    repository.delete(
        "DOC-ES09-001"
    )

    result = repository.get_by_code(
        "DOC-ES09-001"
    )

    assert result is None


def test_should_allow_deleting_nonexistent_document() -> None:
    repository = InMemoryDocumentRepository()

    repository.delete(
        "DOC-NOT-FOUND"
    )

    assert repository.get_by_code(
        "DOC-NOT-FOUND"
    ) is None
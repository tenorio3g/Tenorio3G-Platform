from app.domains.assets.documents.entities import Document

from app.domains.assets.documents.repositories import (
    InMemoryDocumentRepository,
)

from app.domains.assets.documents.use_cases.get_document import (
    GetDocument,
    GetDocumentQuery,
)


def test_should_get_document_by_code() -> None:

    repository = InMemoryDocumentRepository()

    repository.save(
        Document(
            code="DOC-ES09-001",
            asset_code="ES09",
            title="Diagrama unifilar",
            document_type="electrical_diagram",
            file_name="ES09_unifilar.pdf",
        )
    )

    use_case = GetDocument(repository)

    result = use_case.execute(
        GetDocumentQuery(
            code="DOC-ES09-001"
        )
    )

    assert result.document is not None
    assert result.document.code == "DOC-ES09-001"
    assert result.document.asset_code == "ES09"


def test_should_return_none_when_document_does_not_exist() -> None:

    repository = InMemoryDocumentRepository()

    use_case = GetDocument(repository)

    result = use_case.execute(
        GetDocumentQuery(
            code="DOC-NOT-FOUND"
        )
    )

    assert result.document is None
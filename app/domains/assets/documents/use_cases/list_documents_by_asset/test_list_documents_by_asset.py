from app.domains.assets.documents.entities import Document

from app.domains.assets.documents.repositories import (
    InMemoryDocumentRepository,
)

from app.domains.assets.documents.use_cases.list_documents_by_asset import (
    ListDocumentsByAsset,
    ListDocumentsByAssetQuery,
)


def test_should_list_documents_by_asset() -> None:

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

    repository.save(
        Document(
            code="DOC-ES09-002",
            asset_code="ES09",
            title="Diagrama",
            document_type="electrical_diagram",
            file_name="diagram.pdf",
        )
    )

    repository.save(
        Document(
            code="DOC-CH11-001",
            asset_code="CH11",
            title="Manual Chiller",
            document_type="manual",
            file_name="chiller.pdf",
        )
    )

    use_case = ListDocumentsByAsset(
        repository
    )

    result = use_case.execute(
        ListDocumentsByAssetQuery(
            asset_code="ES09"
        )
    )

    assert len(result.documents) == 2

    assert all(
        document.asset_code == "ES09"
        for document in result.documents
    )


def test_should_return_empty_list_when_asset_has_no_documents() -> None:

    repository = InMemoryDocumentRepository()

    use_case = ListDocumentsByAsset(
        repository
    )

    result = use_case.execute(
        ListDocumentsByAssetQuery(
            asset_code="NO-DOCUMENTS"
        )
    )

    assert result.documents == []
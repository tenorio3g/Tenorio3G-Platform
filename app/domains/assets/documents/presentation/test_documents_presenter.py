from app.domains.assets.documents.entities import Document

from app.domains.assets.documents.presentation import (
    DocumentsPresenter,
)


def test_should_present_documents() -> None:

    documents = [
        Document(
            code="DOC-ES09-001",
            asset_code="ES09",
            title="Diagrama unifilar",
            document_type="electrical_diagram",
            file_name="ES09_unifilar.pdf",
            description="Diagrama principal.",
            revision="A",
        )
    ]

    view_model = DocumentsPresenter.present(
        documents
    )

    assert len(view_model.items) == 1

    item = view_model.items[0]

    assert item.code == "DOC-ES09-001"
    assert item.title == "Diagrama unifilar"
    assert item.document_type == "electrical_diagram"
    assert item.file_name == "ES09_unifilar.pdf"
    assert item.description == "Diagrama principal."
    assert item.revision == "A"
    assert item.created_at != ""


def test_should_present_default_values() -> None:

    documents = [
        Document(
            code="DOC-ES09-002",
            asset_code="ES09",
            title="Manual",
            document_type="manual",
            file_name="manual.pdf",
        )
    ]

    view_model = DocumentsPresenter.present(
        documents
    )

    item = view_model.items[0]

    assert item.description == ""
    assert item.revision == "Sin revisión"


def test_should_present_empty_document_list() -> None:

    view_model = DocumentsPresenter.present(
        []
    )

    assert view_model.items == []
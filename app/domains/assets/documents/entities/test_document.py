import pytest

from app.domains.assets.documents.entities import Document


def test_should_create_document() -> None:
    document = Document(
        code="DOC-ES09-001",
        asset_code="ES09",
        title="Diagrama unifilar tablero ES09",
        document_type="electrical_diagram",
        file_name="ES09_unifilar.pdf",
        revision="A",
    )

    assert document.code == "DOC-ES09-001"
    assert document.asset_code == "ES09"
    assert document.title == "Diagrama unifilar tablero ES09"
    assert document.document_type == "electrical_diagram"
    assert document.file_name == "ES09_unifilar.pdf"
    assert document.revision == "A"
    assert document.created_at is not None


def test_should_create_document_with_default_values() -> None:
    document = Document(
        code="DOC-ES09-002",
        asset_code="ES09",
        title="Manual del fabricante",
        document_type="manual",
        file_name="manual_es09.pdf",
    )

    assert document.description == ""
    assert document.revision == ""
    assert document.created_at is not None


@pytest.mark.parametrize(
    ("field", "value", "expected_message"),
    [
        ("code", "", "Document code is required."),
        ("asset_code", "", "Asset code is required."),
        ("title", "", "Document title is required."),
        ("document_type", "", "Document type is required."),
        ("file_name", "", "File name is required."),
    ],
)
def test_should_reject_required_empty_fields(
    field: str,
    value: str,
    expected_message: str,
) -> None:
    data = {
        "code": "DOC-ES09-001",
        "asset_code": "ES09",
        "title": "Diagrama unifilar",
        "document_type": "electrical_diagram",
        "file_name": "ES09_unifilar.pdf",
    }

    data[field] = value

    with pytest.raises(ValueError, match=expected_message):
        Document(**data)
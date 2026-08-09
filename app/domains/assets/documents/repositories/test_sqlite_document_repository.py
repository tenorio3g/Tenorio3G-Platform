from app.foundation.database import Base, engine

from app.domains.assets.documents.entities import Document

from app.domains.assets.documents.models import (
    DocumentModel,
)

from app.domains.assets.documents.repositories.sqlite_document_repository import (
    SQLiteDocumentRepository,
)


def test_should_save_and_get_document() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteDocumentRepository()

    repository.save(
        Document(
            code="TEST-DOC-ES09-001",
            asset_code="ES09",
            title="Diagrama unifilar ES09",
            document_type="electrical_diagram",
            file_name="ES09_unifilar.pdf",
            description="Diagrama eléctrico de prueba.",
            revision="A",
        )
    )

    persisted = repository.get_by_code(
        "TEST-DOC-ES09-001"
    )

    assert persisted is not None
    assert persisted.code == "TEST-DOC-ES09-001"
    assert persisted.asset_code == "ES09"
    assert persisted.title == "Diagrama unifilar ES09"
    assert persisted.document_type == "electrical_diagram"
    assert persisted.file_name == "ES09_unifilar.pdf"
    assert persisted.description == "Diagrama eléctrico de prueba."
    assert persisted.revision == "A"
    assert persisted.created_at is not None


def test_should_return_none_when_document_does_not_exist() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteDocumentRepository()

    persisted = repository.get_by_code(
        "TEST-DOC-NOT-FOUND"
    )

    assert persisted is None


def test_should_get_documents_by_asset_code() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteDocumentRepository()

    repository.save(
        Document(
            code="TEST-DOC-ES09-002",
            asset_code="ES09",
            title="Manual ES09",
            document_type="manual",
            file_name="manual_es09.pdf",
        )
    )

    repository.save(
        Document(
            code="TEST-DOC-ES09-003",
            asset_code="ES09",
            title="Ficha técnica ES09",
            document_type="datasheet",
            file_name="datasheet_es09.pdf",
        )
    )

    repository.save(
        Document(
            code="TEST-DOC-CH11-001",
            asset_code="CH11",
            title="Manual Chiller 11",
            document_type="manual",
            file_name="manual_ch11.pdf",
        )
    )

    documents = repository.get_by_asset_code(
        "ES09"
    )

    codes = {
        document.code
        for document in documents
    }

    assert "TEST-DOC-ES09-002" in codes
    assert "TEST-DOC-ES09-003" in codes
    assert "TEST-DOC-CH11-001" not in codes


def test_should_update_existing_document() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteDocumentRepository()

    repository.save(
        Document(
            code="TEST-DOC-UPDATE-001",
            asset_code="ES09",
            title="Manual original",
            document_type="manual",
            file_name="manual_original.pdf",
            revision="A",
        )
    )

    repository.save(
        Document(
            code="TEST-DOC-UPDATE-001",
            asset_code="ES09",
            title="Manual actualizado",
            document_type="manual",
            file_name="manual_actualizado.pdf",
            description="Documento actualizado.",
            revision="B",
        )
    )

    persisted = repository.get_by_code(
        "TEST-DOC-UPDATE-001"
    )

    assert persisted is not None
    assert persisted.title == "Manual actualizado"
    assert persisted.file_name == "manual_actualizado.pdf"
    assert persisted.description == "Documento actualizado."
    assert persisted.revision == "B"


def test_should_delete_document() -> None:

    Base.metadata.create_all(engine)

    repository = SQLiteDocumentRepository()

    repository.save(
        Document(
            code="TEST-DOC-DELETE-001",
            asset_code="ES09",
            title="Documento para eliminar",
            document_type="manual",
            file_name="delete_test.pdf",
        )
    )

    repository.delete(
        "TEST-DOC-DELETE-001"
    )

    persisted = repository.get_by_code(
        "TEST-DOC-DELETE-001"
    )

    assert persisted is None
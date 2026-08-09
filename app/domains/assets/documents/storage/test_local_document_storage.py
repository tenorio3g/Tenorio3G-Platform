from pathlib import Path

from app.domains.assets.documents.storage import (
    LocalDocumentStorage,
)


def test_should_save_document(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.pdf"
    source.write_bytes(
        b"PDF de prueba"
    )

    storage_path = (
        tmp_path
        / "documents"
    )

    storage = LocalDocumentStorage(
        storage_path
    )

    destination = storage.save(
        source,
        "manual.pdf",
    )

    assert destination.exists()
    assert destination.name == "manual.pdf"

    assert destination.read_bytes() == (
        b"PDF de prueba"
    )


def test_should_detect_existing_document(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.pdf"
    source.write_bytes(
        b"PDF de prueba"
    )

    storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    storage.save(
        source,
        "manual.pdf",
    )

    assert storage.exists(
        "manual.pdf"
    ) is True

    assert storage.exists(
        "no_existe.pdf"
    ) is False


def test_should_delete_document(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.pdf"
    source.write_bytes(
        b"PDF de prueba"
    )

    storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    storage.save(
        source,
        "manual.pdf",
    )

    assert storage.exists(
        "manual.pdf"
    ) is True

    storage.delete(
        "manual.pdf"
    )

    assert storage.exists(
        "manual.pdf"
    ) is False

def test_should_return_document_path(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.pdf"
    source.write_bytes(
        b"PDF de prueba"
    )

    storage = LocalDocumentStorage(
        tmp_path / "documents"
    )

    storage.save(
        source,
        "manual.pdf",
    )

    file_path = storage.get_path(
        "manual.pdf"
    )

    assert file_path.exists()
    assert file_path.name == "manual.pdf"
    assert file_path.read_bytes() == b"PDF de prueba"
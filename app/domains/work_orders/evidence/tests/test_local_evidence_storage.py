from pathlib import Path

import pytest

from app.domains.work_orders.evidence.storage import (
    LocalEvidenceStorage,
)


def test_should_save_evidence_file(
    tmp_path: Path,
):

    source = (
        tmp_path
        / "source.jpg"
    )

    source.write_bytes(
        b"fake evidence data"
    )

    storage = LocalEvidenceStorage(
        tmp_path
        / "evidence"
    )

    destination = storage.save(
        source,
        "EVID-001.jpg",
    )

    assert destination.exists()

    assert (
        destination.name
        == "EVID-001.jpg"
    )

    assert (
        destination.read_bytes()
        == b"fake evidence data"
    )


def test_should_detect_existing_file(
    tmp_path: Path,
):

    source = (
        tmp_path
        / "source.jpg"
    )

    source.write_bytes(
        b"evidence"
    )

    storage = LocalEvidenceStorage(
        tmp_path
        / "evidence"
    )

    storage.save(
        source,
        "EVID-001.jpg",
    )

    assert (
        storage.exists(
            "EVID-001.jpg"
        )
        is True
    )

    assert (
        storage.exists(
            "missing.jpg"
        )
        is False
    )


def test_should_return_evidence_path(
    tmp_path: Path,
):

    source = (
        tmp_path
        / "source.pdf"
    )

    source.write_bytes(
        b"fake pdf"
    )

    storage = LocalEvidenceStorage(
        tmp_path
        / "evidence"
    )

    storage.save(
        source,
        "EVID-002.pdf",
    )

    file_path = storage.get_path(
        "EVID-002.pdf"
    )

    assert file_path.exists()

    assert (
        file_path.name
        == "EVID-002.pdf"
    )


def test_should_delete_evidence_file(
    tmp_path: Path,
):

    source = (
        tmp_path
        / "source.jpg"
    )

    source.write_bytes(
        b"evidence"
    )

    storage = LocalEvidenceStorage(
        tmp_path
        / "evidence"
    )

    storage.save(
        source,
        "EVID-001.jpg",
    )

    assert storage.exists(
        "EVID-001.jpg"
    )

    storage.delete(
        "EVID-001.jpg"
    )

    assert storage.exists(
        "EVID-001.jpg"
    ) is False


def test_should_reject_missing_source(
    tmp_path: Path,
):

    storage = LocalEvidenceStorage(
        tmp_path
        / "evidence"
    )

    with pytest.raises(
        FileNotFoundError
    ):
        storage.save(
            tmp_path / "missing.jpg",
            "EVID-001.jpg",
        )


def test_should_strip_path_from_stored_name(
    tmp_path: Path,
):

    source = (
        tmp_path
        / "source.jpg"
    )

    source.write_bytes(
        b"safe evidence"
    )

    storage = LocalEvidenceStorage(
        tmp_path
        / "evidence"
    )

    destination = storage.save(
        source,
        "../../EVID-003.jpg",
    )

    assert (
        destination.parent
        == (tmp_path / "evidence").resolve()
    )

    assert (
        destination.name
        == "EVID-003.jpg"
    )
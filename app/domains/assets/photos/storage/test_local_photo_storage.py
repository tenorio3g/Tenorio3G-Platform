from pathlib import Path

from app.domains.assets.photos.storage import (
    LocalPhotoStorage,
)


def test_should_save_photo(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.jpg"

    source.write_bytes(
        b"fake image data"
    )

    storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    destination = storage.save(
        source,
        "photo.jpg",
    )

    assert destination.exists()
    assert destination.name == "photo.jpg"

    assert destination.read_bytes() == (
        b"fake image data"
    )


def test_should_detect_existing_photo(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.jpg"

    source.write_bytes(
        b"fake image data"
    )

    storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    storage.save(
        source,
        "photo.jpg",
    )

    assert storage.exists(
        "photo.jpg"
    ) is True

    assert storage.exists(
        "missing.jpg"
    ) is False


def test_should_return_photo_path(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.jpg"

    source.write_bytes(
        b"fake image data"
    )

    storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    storage.save(
        source,
        "photo.jpg",
    )

    file_path = storage.get_path(
        "photo.jpg"
    )

    assert file_path.exists()
    assert file_path.name == "photo.jpg"


def test_should_delete_photo(
    tmp_path: Path,
) -> None:

    source = tmp_path / "source.jpg"

    source.write_bytes(
        b"fake image data"
    )

    storage = LocalPhotoStorage(
        tmp_path / "photos"
    )

    storage.save(
        source,
        "photo.jpg",
    )

    assert storage.exists(
        "photo.jpg"
    ) is True

    storage.delete(
        "photo.jpg"
    )

    assert storage.exists(
        "photo.jpg"
    ) is False
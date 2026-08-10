from app.domains.assets.photos.entities import Photo

from app.domains.assets.photos.repositories import (
    InMemoryPhotoRepository,
)


def create_photo(
    code: str = "PHOTO-ES09-001",
    asset_code: str = "S2-480-ES09-T269",
) -> Photo:

    return Photo(
        code=code,
        asset_code=asset_code,
        title="Fotografía técnica",
        photo_type="general",
        file_name=f"{code}.jpg",
    )


def test_should_save_and_get_photo() -> None:

    repository = InMemoryPhotoRepository()

    photo = create_photo()

    repository.save(photo)

    persisted = repository.get_by_code(
        "PHOTO-ES09-001"
    )

    assert persisted is photo


def test_should_return_none_when_photo_does_not_exist() -> None:

    repository = InMemoryPhotoRepository()

    persisted = repository.get_by_code(
        "PHOTO-NOT-FOUND"
    )

    assert persisted is None


def test_should_get_photos_by_asset_code() -> None:

    repository = InMemoryPhotoRepository()

    repository.save(
        create_photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
        )
    )

    repository.save(
        create_photo(
            code="PHOTO-ES09-002",
            asset_code="S2-480-ES09-T269",
        )
    )

    repository.save(
        create_photo(
            code="PHOTO-CH11-001",
            asset_code="CH11",
        )
    )

    photos = repository.get_by_asset_code(
        "S2-480-ES09-T269"
    )

    assert len(photos) == 2

    assert all(
        photo.asset_code == "S2-480-ES09-T269"
        for photo in photos
    )


def test_should_delete_photo() -> None:

    repository = InMemoryPhotoRepository()

    repository.save(
        create_photo()
    )

    repository.delete(
        "PHOTO-ES09-001"
    )

    assert repository.get_by_code(
        "PHOTO-ES09-001"
    ) is None


def test_should_allow_deleting_nonexistent_photo() -> None:

    repository = InMemoryPhotoRepository()

    repository.delete(
        "PHOTO-NOT-FOUND"
    )

    assert repository.get_by_code(
        "PHOTO-NOT-FOUND"
    ) is None
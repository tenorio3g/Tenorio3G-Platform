from app.domains.assets.photos.entities import Photo

from app.domains.assets.photos.repositories import (
    InMemoryPhotoRepository,
)

from app.domains.assets.photos.use_cases import (
    DeletePhoto,
    DeletePhotoCommand,
)


def test_should_delete_existing_photo() -> None:

    repository = InMemoryPhotoRepository()

    repository.save(
        Photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Foto general",
            photo_type="general",
            file_name="foto.jpg",
        )
    )

    use_case = DeletePhoto(
        repository
    )

    result = use_case.execute(
        DeletePhotoCommand(
            code="PHOTO-ES09-001"
        )
    )

    assert result.success is True

    assert repository.get_by_code(
        "PHOTO-ES09-001"
    ) is None


def test_should_not_delete_nonexistent_photo() -> None:

    repository = InMemoryPhotoRepository()

    use_case = DeletePhoto(
        repository
    )

    result = use_case.execute(
        DeletePhotoCommand(
            code="PHOTO-NOT-FOUND"
        )
    )

    assert result.success is False
    assert result.error == "Photo not found."
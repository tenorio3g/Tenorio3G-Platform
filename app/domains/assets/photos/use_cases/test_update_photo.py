from app.domains.assets.photos.entities import Photo

from app.domains.assets.photos.repositories import (
    InMemoryPhotoRepository,
)

from app.domains.assets.photos.use_cases import (
    UpdatePhoto,
    UpdatePhotoCommand,
)


def test_should_update_existing_photo() -> None:

    repository = InMemoryPhotoRepository()

    original = Photo(
        code="PHOTO-ES09-001",
        asset_code="S2-480-ES09-T269",
        title="Foto original",
        photo_type="general",
        file_name="original.jpg",
        description="Original.",
    )

    repository.save(original)

    original_created_at = original.created_at

    use_case = UpdatePhoto(
        repository
    )

    result = use_case.execute(
        UpdatePhotoCommand(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Foto actualizada",
            photo_type="nameplate",
            file_name="actualizada.jpg",
            description="Descripción actualizada.",
        )
    )

    assert result.success is True
    assert result.photo is not None

    assert result.photo.title == "Foto actualizada"
    assert result.photo.photo_type == "nameplate"
    assert result.photo.file_name == "actualizada.jpg"
    assert (
        result.photo.created_at
        == original_created_at
    )

    persisted = repository.get_by_code(
        "PHOTO-ES09-001"
    )

    assert persisted is not None
    assert persisted.title == "Foto actualizada"


def test_should_not_update_nonexistent_photo() -> None:

    repository = InMemoryPhotoRepository()

    use_case = UpdatePhoto(
        repository
    )

    result = use_case.execute(
        UpdatePhotoCommand(
            code="PHOTO-NOT-FOUND",
            asset_code="S2-480-ES09-T269",
            title="Foto",
            photo_type="general",
            file_name="foto.jpg",
        )
    )

    assert result.success is False
    assert result.photo is None
    assert result.error == "Photo not found."


def test_should_reject_invalid_update() -> None:

    repository = InMemoryPhotoRepository()

    repository.save(
        Photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Foto original",
            photo_type="general",
            file_name="original.jpg",
        )
    )

    use_case = UpdatePhoto(
        repository
    )

    result = use_case.execute(
        UpdatePhotoCommand(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="",
            photo_type="general",
            file_name="foto.jpg",
        )
    )

    assert result.success is False
    assert result.photo is None
    assert result.error == "Photo title is required."
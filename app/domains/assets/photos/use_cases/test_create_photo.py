from app.domains.assets.photos.repositories import (
    InMemoryPhotoRepository,
)

from app.domains.assets.photos.use_cases import (
    CreatePhoto,
    CreatePhotoCommand,
)


def test_should_create_photo() -> None:

    repository = InMemoryPhotoRepository()

    use_case = CreatePhoto(
        repository
    )

    result = use_case.execute(
        CreatePhotoCommand(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
            description="Placa del tablero.",
        )
    )

    assert result.success is True
    assert result.photo is not None

    persisted = repository.get_by_code(
        "PHOTO-ES09-001"
    )

    assert persisted is not None
    assert persisted.title == "Placa de datos"


def test_should_reject_duplicate_photo() -> None:

    repository = InMemoryPhotoRepository()

    use_case = CreatePhoto(
        repository
    )

    command = CreatePhotoCommand(
        code="PHOTO-ES09-001",
        asset_code="S2-480-ES09-T269",
        title="Placa de datos",
        photo_type="nameplate",
        file_name="placa.jpg",
    )

    first_result = use_case.execute(
        command
    )

    second_result = use_case.execute(
        command
    )

    assert first_result.success is True
    assert second_result.success is False
    assert (
        second_result.error
        == "Photo already exists."
    )


def test_should_reject_invalid_photo() -> None:

    repository = InMemoryPhotoRepository()

    use_case = CreatePhoto(
        repository
    )

    result = use_case.execute(
        CreatePhotoCommand(
            code="",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
        )
    )

    assert result.success is False
    assert result.photo is None
    assert (
        result.error
        == "Photo code is required."
    )
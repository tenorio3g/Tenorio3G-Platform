from app.domains.assets.photos.entities import Photo

from app.domains.assets.photos.repositories import (
    InMemoryPhotoRepository,
)

from app.domains.assets.photos.use_cases import (
    GetPhoto,
    GetPhotoQuery,
)


def test_should_get_photo() -> None:

    repository = InMemoryPhotoRepository()

    repository.save(
        Photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
        )
    )

    use_case = GetPhoto(
        repository
    )

    result = use_case.execute(
        GetPhotoQuery(
            code="PHOTO-ES09-001"
        )
    )

    assert result.photo is not None
    assert result.photo.code == "PHOTO-ES09-001"
    assert result.photo.title == "Placa de datos"


def test_should_return_none_when_photo_does_not_exist() -> None:

    repository = InMemoryPhotoRepository()

    use_case = GetPhoto(
        repository
    )

    result = use_case.execute(
        GetPhotoQuery(
            code="PHOTO-NOT-FOUND"
        )
    )

    assert result.photo is None
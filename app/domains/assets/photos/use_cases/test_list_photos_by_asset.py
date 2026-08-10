from app.domains.assets.photos.entities import Photo

from app.domains.assets.photos.repositories import (
    InMemoryPhotoRepository,
)

from app.domains.assets.photos.use_cases import (
    ListPhotosByAsset,
    ListPhotosByAssetQuery,
)


def test_should_list_photos_by_asset() -> None:

    repository = InMemoryPhotoRepository()

    repository.save(
        Photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Foto general",
            photo_type="general",
            file_name="general.jpg",
        )
    )

    repository.save(
        Photo(
            code="PHOTO-ES09-002",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
        )
    )

    repository.save(
        Photo(
            code="PHOTO-CH11-001",
            asset_code="CH11",
            title="Foto chiller",
            photo_type="general",
            file_name="chiller.jpg",
        )
    )

    use_case = ListPhotosByAsset(
        repository
    )

    result = use_case.execute(
        ListPhotosByAssetQuery(
            asset_code="S2-480-ES09-T269"
        )
    )

    assert len(result.photos) == 2

    assert {
        photo.code
        for photo in result.photos
    } == {
        "PHOTO-ES09-001",
        "PHOTO-ES09-002",
    }


def test_should_return_empty_list_when_asset_has_no_photos() -> None:

    repository = InMemoryPhotoRepository()

    use_case = ListPhotosByAsset(
        repository
    )

    result = use_case.execute(
        ListPhotosByAssetQuery(
            asset_code="ASSET-WITHOUT-PHOTOS"
        )
    )

    assert result.photos == []
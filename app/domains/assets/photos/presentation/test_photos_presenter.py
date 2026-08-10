from app.domains.assets.photos.entities import Photo
from datetime import datetime
from app.domains.assets.photos.presentation import (
    PhotosPresenter,
)


def test_should_present_photos() -> None:

    photos = [
        Photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
            description="Placa de identificación.",
        )
    ]

    view_model = PhotosPresenter.present(
        photos
    )

    assert view_model.has_items is True
    assert len(view_model.items) == 1

    item = view_model.items[0]

    assert item.code == "PHOTO-ES09-001"
    assert item.title == "Placa de datos"
    assert item.photo_type == "nameplate"
    assert item.file_name == "placa.jpg"
    assert item.description == "Placa de identificación."
    assert item.created_at != ""


def test_should_present_empty_photo_list() -> None:

    view_model = PhotosPresenter.present(
        []
    )

    assert view_model.has_items is False
    assert view_model.items == []

def test_should_identify_general_photo_as_primary() -> None:

    photos = [
        Photo(
            code="PHOTO-ES09-001",
            asset_code="S2-480-ES09-T269",
            title="Placa",
            photo_type="nameplate",
            file_name="placa.jpg",
        ),
        Photo(
            code="PHOTO-ES09-002",
            asset_code="S2-480-ES09-T269",
            title="Foto general",
            photo_type="general",
            file_name="general.jpg",
        ),
    ]

    view_model = PhotosPresenter.present(
        photos
    )

    assert view_model.primary_photo is not None
    assert (
        view_model.primary_photo.code
        == "PHOTO-ES09-002"
    )
def test_should_use_most_recent_general_photo_as_primary() -> None:

    photos = [
        Photo(
            code="PHOTO-GENERAL-OLD",
            asset_code="S2-480-ES09-T269",
            title="Foto general anterior",
            photo_type="general",
            file_name="old.jpg",
            created_at=datetime(
                2026,
                8,
                1,
                10,
                0,
            ),
        ),
        Photo(
            code="PHOTO-GENERAL-NEW",
            asset_code="S2-480-ES09-T269",
            title="Foto general reciente",
            photo_type="general",
            file_name="new.jpg",
            created_at=datetime(
                2026,
                8,
                9,
                18,
                0,
            ),
        ),
    ]

    view_model = PhotosPresenter.present(
        photos
    )

    assert view_model.primary_photo is not None

    assert (
        view_model.primary_photo.code
        == "PHOTO-GENERAL-NEW"
    )
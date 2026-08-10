import pytest

from app.domains.assets.photos.entities.photo import Photo


def test_create_photo() -> None:
    photo = Photo(
        code="PHOTO-ES09-001",
        asset_code="S2-480-ES09-T269",
        title="Placa de datos tablero ES09",
        photo_type="nameplate",
        file_name="PHOTO-ES09-001__placa.jpg",
        description="Placa de identificación.",
    )

    assert photo.code == "PHOTO-ES09-001"
    assert photo.asset_code == "S2-480-ES09-T269"
    assert photo.title == "Placa de datos tablero ES09"
    assert photo.photo_type == "nameplate"
    assert photo.file_name == "PHOTO-ES09-001__placa.jpg"
    assert photo.description == "Placa de identificación."
    assert photo.created_at is not None


def test_photo_requires_code() -> None:
    with pytest.raises(
        ValueError,
        match="Photo code is required.",
    ):
        Photo(
            code="",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
        )


def test_photo_requires_asset_code() -> None:
    with pytest.raises(
        ValueError,
        match="Asset code is required.",
    ):
        Photo(
            code="PHOTO-001",
            asset_code="",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="placa.jpg",
        )


def test_photo_requires_title() -> None:
    with pytest.raises(
        ValueError,
        match="Photo title is required.",
    ):
        Photo(
            code="PHOTO-001",
            asset_code="S2-480-ES09-T269",
            title="",
            photo_type="nameplate",
            file_name="placa.jpg",
        )


def test_photo_requires_photo_type() -> None:
    with pytest.raises(
        ValueError,
        match="Photo type is required.",
    ):
        Photo(
            code="PHOTO-001",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="",
            file_name="placa.jpg",
        )


def test_photo_requires_file_name() -> None:
    with pytest.raises(
        ValueError,
        match="File name is required.",
    ):
        Photo(
            code="PHOTO-001",
            asset_code="S2-480-ES09-T269",
            title="Placa de datos",
            photo_type="nameplate",
            file_name="",
        )
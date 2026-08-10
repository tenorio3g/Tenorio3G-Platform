from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.photos.entities import Photo
from app.domains.assets.photos.models import PhotoModel
from app.domains.assets.photos.repositories import (
    SQLitePhotoRepository,
)


def create_repository():
    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(
        bind=engine
    )

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    return SQLitePhotoRepository(
        session_factory=session_factory
    )


def create_photo(
    code: str = "PHOTO-ES09-001",
    asset_code: str = "S2-480-ES09-T269",
) -> Photo:

    return Photo(
        code=code,
        asset_code=asset_code,
        title="Placa de datos ES09",
        photo_type="nameplate",
        file_name=f"{code}__placa.jpg",
        description="Fotografía técnica.",
        created_at=datetime(
            2026,
            8,
            9,
            10,
            0,
        ),
    )


def test_sqlite_repository_should_save_and_get_photo() -> None:

    repository = create_repository()

    photo = create_photo()

    repository.save(photo)

    persisted = repository.get_by_code(
        "PHOTO-ES09-001"
    )

    assert persisted is not None

    assert persisted.code == photo.code
    assert persisted.asset_code == photo.asset_code
    assert persisted.title == photo.title
    assert persisted.photo_type == photo.photo_type
    assert persisted.file_name == photo.file_name
    assert persisted.description == photo.description
    assert persisted.created_at == photo.created_at


def test_sqlite_repository_should_return_none_when_not_found() -> None:

    repository = create_repository()

    result = repository.get_by_code(
        "PHOTO-NOT-FOUND"
    )

    assert result is None


def test_sqlite_repository_should_get_photos_by_asset() -> None:

    repository = create_repository()

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

    assert {
        photo.code
        for photo in photos
    } == {
        "PHOTO-ES09-001",
        "PHOTO-ES09-002",
    }


def test_sqlite_repository_should_update_photo() -> None:

    repository = create_repository()

    photo = create_photo()

    repository.save(photo)

    updated_photo = Photo(
        code="PHOTO-ES09-001",
        asset_code="S2-480-ES09-T269",
        title="Placa actualizada",
        photo_type="nameplate",
        file_name="PHOTO-ES09-001__nueva.jpg",
        description="Descripción actualizada.",
        created_at=photo.created_at,
    )

    repository.save(
        updated_photo
    )

    persisted = repository.get_by_code(
        "PHOTO-ES09-001"
    )

    assert persisted is not None
    assert persisted.title == "Placa actualizada"
    assert (
        persisted.file_name
        == "PHOTO-ES09-001__nueva.jpg"
    )
    assert (
        persisted.description
        == "Descripción actualizada."
    )


def test_sqlite_repository_should_delete_photo() -> None:

    repository = create_repository()

    repository.save(
        create_photo()
    )

    repository.delete(
        "PHOTO-ES09-001"
    )

    persisted = repository.get_by_code(
        "PHOTO-ES09-001"
    )

    assert persisted is None
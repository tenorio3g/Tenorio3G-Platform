from __future__ import annotations

from sqlalchemy import select

from app.foundation.database import SessionLocal

from app.domains.assets.photos.entities import Photo
from app.domains.assets.photos.models import PhotoModel
from app.domains.assets.photos.repositories.photo_repository import (
    PhotoRepository,
)


class SQLitePhotoRepository(
    PhotoRepository,
):

    def __init__(
        self,
        session_factory=SessionLocal,
    ) -> None:
        self._session_factory = session_factory

    def save(
        self,
        photo: Photo,
    ) -> None:

        clean_code = photo.code.strip()

        with self._session_factory() as session:

            model = session.scalar(
                select(PhotoModel).where(
                    PhotoModel.code == clean_code
                )
            )

            if model is None:

                model = PhotoModel(
                    code=clean_code,
                    asset_code=photo.asset_code.strip(),
                    title=photo.title,
                    photo_type=photo.photo_type,
                    file_name=photo.file_name,
                    description=photo.description,
                    created_at=photo.created_at,
                )

                session.add(model)

            else:

                model.asset_code = photo.asset_code.strip()
                model.title = photo.title
                model.photo_type = photo.photo_type
                model.file_name = photo.file_name
                model.description = photo.description
                model.created_at = photo.created_at

            session.commit()

    def get_by_code(
        self,
        code: str,
    ) -> Photo | None:

        clean_code = code.strip()

        if not clean_code:
            return None

        with self._session_factory() as session:

            model = session.scalar(
                select(PhotoModel).where(
                    PhotoModel.code == clean_code
                )
            )

            if model is None:
                return None

            return self._to_entity(model)

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[Photo]:

        clean_asset_code = asset_code.strip()

        if not clean_asset_code:
            return []

        with self._session_factory() as session:

            models = list(
                session.scalars(
                    select(PhotoModel).where(
                        PhotoModel.asset_code
                        == clean_asset_code
                    )
                ).all()
            )

            return [
                self._to_entity(model)
                for model in models
            ]

    def delete(
        self,
        code: str,
    ) -> None:

        clean_code = code.strip()

        if not clean_code:
            return

        with self._session_factory() as session:

            model = session.scalar(
                select(PhotoModel).where(
                    PhotoModel.code == clean_code
                )
            )

            if model is None:
                return

            session.delete(model)
            session.commit()

    @staticmethod
    def _to_entity(
        model: PhotoModel,
    ) -> Photo:

        return Photo(
            code=model.code,
            asset_code=model.asset_code,
            title=model.title,
            photo_type=model.photo_type,
            file_name=model.file_name,
            description=model.description,
            created_at=model.created_at,
        )
from dataclasses import dataclass

from app.domains.assets.photos.entities import Photo
from app.domains.assets.photos.repositories import (
    PhotoRepository,
)


@dataclass
class CreatePhotoCommand:
    code: str
    asset_code: str
    title: str
    photo_type: str
    file_name: str
    description: str = ""


@dataclass
class CreatePhotoResult:
    success: bool
    photo: Photo | None = None
    error: str | None = None


class CreatePhoto:

    def __init__(
        self,
        repository: PhotoRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: CreatePhotoCommand,
    ) -> CreatePhotoResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is not None:
            return CreatePhotoResult(
                success=False,
                error="Photo already exists.",
            )

        try:
            photo = Photo(
                code=command.code,
                asset_code=command.asset_code,
                title=command.title,
                photo_type=command.photo_type,
                file_name=command.file_name,
                description=command.description,
            )

        except ValueError as exc:
            return CreatePhotoResult(
                success=False,
                error=str(exc),
            )

        self._repository.save(photo)

        return CreatePhotoResult(
            success=True,
            photo=photo,
        )
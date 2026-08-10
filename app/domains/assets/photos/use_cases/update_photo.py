from dataclasses import dataclass

from app.domains.assets.photos.entities import Photo
from app.domains.assets.photos.repositories import (
    PhotoRepository,
)


@dataclass
class UpdatePhotoCommand:
    code: str
    asset_code: str
    title: str
    photo_type: str
    file_name: str
    description: str = ""


@dataclass
class UpdatePhotoResult:
    success: bool
    photo: Photo | None = None
    error: str | None = None


class UpdatePhoto:

    def __init__(
        self,
        repository: PhotoRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: UpdatePhotoCommand,
    ) -> UpdatePhotoResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            return UpdatePhotoResult(
                success=False,
                error="Photo not found.",
            )

        try:
            photo = Photo(
                code=command.code,
                asset_code=command.asset_code,
                title=command.title,
                photo_type=command.photo_type,
                file_name=command.file_name,
                description=command.description,
                created_at=existing.created_at,
            )

        except ValueError as exc:
            return UpdatePhotoResult(
                success=False,
                error=str(exc),
            )

        self._repository.save(photo)

        return UpdatePhotoResult(
            success=True,
            photo=photo,
        )
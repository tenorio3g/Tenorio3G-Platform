from dataclasses import dataclass

from app.domains.assets.photos.repositories import (
    PhotoRepository,
)


@dataclass
class DeletePhotoCommand:
    code: str


@dataclass
class DeletePhotoResult:
    success: bool
    error: str | None = None


class DeletePhoto:

    def __init__(
        self,
        repository: PhotoRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: DeletePhotoCommand,
    ) -> DeletePhotoResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is None:
            return DeletePhotoResult(
                success=False,
                error="Photo not found.",
            )

        self._repository.delete(
            command.code
        )

        return DeletePhotoResult(
            success=True
        )
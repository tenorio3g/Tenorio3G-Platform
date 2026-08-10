from dataclasses import dataclass

from app.domains.assets.photos.entities import Photo
from app.domains.assets.photos.repositories import (
    PhotoRepository,
)


@dataclass
class GetPhotoQuery:
    code: str


@dataclass
class GetPhotoResult:
    photo: Photo | None


class GetPhoto:

    def __init__(
        self,
        repository: PhotoRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: GetPhotoQuery,
    ) -> GetPhotoResult:

        photo = self._repository.get_by_code(
            query.code
        )

        return GetPhotoResult(
            photo=photo
        )
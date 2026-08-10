from dataclasses import dataclass

from app.domains.assets.photos.entities import Photo
from app.domains.assets.photos.repositories import (
    PhotoRepository,
)


@dataclass
class ListPhotosByAssetQuery:
    asset_code: str


@dataclass
class ListPhotosByAssetResult:
    photos: list[Photo]


class ListPhotosByAsset:

    def __init__(
        self,
        repository: PhotoRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        query: ListPhotosByAssetQuery,
    ) -> ListPhotosByAssetResult:

        photos = self._repository.get_by_asset_code(
            query.asset_code
        )

        return ListPhotosByAssetResult(
            photos=photos
        )
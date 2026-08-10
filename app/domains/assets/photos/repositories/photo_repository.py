from abc import ABC, abstractmethod

from app.domains.assets.photos.entities import Photo


class PhotoRepository(ABC):

    @abstractmethod
    def save(
        self,
        photo: Photo,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(
        self,
        code: str,
    ) -> Photo | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[Photo]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        code: str,
    ) -> None:
        raise NotImplementedError


class InMemoryPhotoRepository(
    PhotoRepository,
):

    def __init__(self) -> None:
        self._photos: dict[str, Photo] = {}

    def save(
        self,
        photo: Photo,
    ) -> None:
        self._photos[photo.code] = photo

    def get_by_code(
        self,
        code: str,
    ) -> Photo | None:
        return self._photos.get(code)

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> list[Photo]:

        return [
            photo
            for photo in self._photos.values()
            if photo.asset_code == asset_code
        ]

    def delete(
        self,
        code: str,
    ) -> None:
        self._photos.pop(
            code,
            None,
        )
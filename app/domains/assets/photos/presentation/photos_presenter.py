from datetime import datetime

from app.domains.assets.photos.entities import Photo

from .photos_view_model import (
    PhotoItemViewModel,
    PhotosViewModel,
)


class PhotosPresenter:
    """
    Adapta fotografías técnicas
    para mostrarlas en el expediente del activo.
    """

    @staticmethod
    def present(
        photos: list[Photo],
    ) -> PhotosViewModel:

        ordered_photos = sorted(
            photos,
            key=lambda photo: (
                photo.created_at
                if photo.created_at is not None
                else datetime.min
            ),
            reverse=True,
        )

        items = [
            PhotoItemViewModel(
                code=photo.code,
                title=photo.title,
                photo_type=photo.photo_type,
                file_name=photo.file_name,
                description=photo.description or "",
                created_at=(
                    photo.created_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                    if photo.created_at
                    else "Sin fecha"
                ),
            )
            for photo in ordered_photos
        ]

        return PhotosViewModel(
            items=items
        )
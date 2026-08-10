from app.domains.assets.photos.repositories import (
    SQLitePhotoRepository,
)

from app.domains.assets.photos.use_cases import (
    CreatePhoto,
    DeletePhoto,
    GetPhoto,
    ListPhotosByAsset,
    UpdatePhoto,
)

from pathlib import Path

from app.domains.assets.photos.storage import (
    LocalPhotoStorage,
)


photo_repository = SQLitePhotoRepository()
photo_storage = LocalPhotoStorage(
    Path("storage/photos")
)


create_photo = CreatePhoto(
    photo_repository,
)

get_photo = GetPhoto(
    photo_repository,
)

list_photos_by_asset = ListPhotosByAsset(
    photo_repository,
)

update_photo = UpdatePhoto(
    photo_repository,
)

delete_photo = DeletePhoto(
    photo_repository,
)
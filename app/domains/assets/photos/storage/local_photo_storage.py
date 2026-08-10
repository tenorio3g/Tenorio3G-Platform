from pathlib import Path
import shutil

from .photo_storage import PhotoStorage


class LocalPhotoStorage(PhotoStorage):
    """
    Almacena fotografías técnicas
    en el sistema de archivos local.
    """

    def __init__(
        self,
        base_path: Path,
    ) -> None:

        self._base_path = Path(
            base_path
        ).resolve()

        self._base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        source_path: Path,
        stored_name: str,
    ) -> Path:

        source_path = Path(
            source_path
        )

        if not source_path.exists():
            raise FileNotFoundError(
                f"Archivo no encontrado: {source_path}"
            )

        destination = (
            self._base_path
            / stored_name
        )

        shutil.copy2(
            source_path,
            destination,
        )

        return destination

    def exists(
        self,
        stored_name: str,
    ) -> bool:

        return (
            self._base_path
            / stored_name
        ).exists()

    def get_path(
        self,
        stored_name: str,
    ) -> Path:

        return (
            self._base_path
            / stored_name
        )

    def delete(
        self,
        stored_name: str,
    ) -> None:

        file_path = (
            self._base_path
            / stored_name
        )

        if file_path.exists():
            file_path.unlink()
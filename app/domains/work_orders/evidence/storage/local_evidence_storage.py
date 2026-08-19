from pathlib import Path
import shutil

from .evidence_storage import (
    EvidenceStorage,
)


class LocalEvidenceStorage(
    EvidenceStorage,
):

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

        safe_name = Path(
            stored_name
        ).name

        if not safe_name:
            raise ValueError(
                "stored_name is required"
            )

        destination = (
            self._base_path
            / safe_name
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

        safe_name = Path(
            stored_name
        ).name

        return (
            self._base_path
            / safe_name
        ).exists()

    def get_path(
        self,
        stored_name: str,
    ) -> Path:

        safe_name = Path(
            stored_name
        ).name

        return (
            self._base_path
            / safe_name
        )

    def delete(
        self,
        stored_name: str,
    ) -> None:

        safe_name = Path(
            stored_name
        ).name

        file_path = (
            self._base_path
            / safe_name
        )

        if file_path.exists():
            file_path.unlink()
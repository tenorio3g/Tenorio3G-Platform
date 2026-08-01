from __future__ import annotations

from pathlib import Path


class Filesystem:
    """
    Utilidad para operaciones básicas del sistema de archivos.

    Esta clase no conoce módulos, plantillas ni reglas de negocio.
    """

    @staticmethod
    def create_directory(path: str | Path) -> Path:
        """
        Crea un directorio, incluyendo padres faltantes.

        Devuelve la ruta creada.
        """

        directory = Path(path)
        directory.mkdir(parents=True, exist_ok=True)

        return directory

    @staticmethod
    def create_file(
        path: str | Path,
        content: str = "",
    ) -> Path:
        """
        Crea un archivo y sus directorios padre.

        Si el archivo ya existe, conserva su contenido.
        """

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if not file_path.exists():
            file_path.write_text(
                content,
                encoding="utf-8",
            )

        return file_path

    @staticmethod
    def write_text(
        path: str | Path,
        content: str,
    ) -> Path:
        """
        Escribe o reemplaza el contenido de un archivo.
        """

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(
            content,
            encoding="utf-8",
        )

        return file_path

    @staticmethod
    def exists(path: str | Path) -> bool:
        """
        Indica si la ruta existe.
        """

        return Path(path).exists()
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FindAllAssetsQuery:
    """
    Consulta para obtener todos los activos registrados.

    Actualmente no requiere parámetros.
    """
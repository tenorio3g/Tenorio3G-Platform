from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FindAssetByCodeQuery:
    """
    Datos necesarios para buscar un activo por código.
    """

    code: str
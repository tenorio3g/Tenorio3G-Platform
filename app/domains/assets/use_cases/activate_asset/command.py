from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ActivateAssetCommand:
    """
    Instrucción para activar un activo.
    """

    code: str
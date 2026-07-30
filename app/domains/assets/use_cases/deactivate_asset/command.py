from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class DeactivateAssetCommand:
    """
    Instrucción para desactivar un activo.

    El motivo es obligatorio porque forma parte
    de la trazabilidad operacional del equipo.
    """

    code: str
    reason: str
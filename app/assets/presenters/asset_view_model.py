from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AssetViewModel:
    """
    Representación de un activo preparada para las plantillas Jinja.

    Los nombres de los atributos corresponden a lo que actualmente
    espera la interfaz web.
    """

    codigo: str
    nombre: str
    estado: str
    ubicacion: str | None
    area: str | None
    ultimo_mantenimiento: str | None
    proximo_mantenimiento: str | None
    salud: int | None
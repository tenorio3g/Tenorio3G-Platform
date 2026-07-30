"""
T3G-ASSET-UC-002

FindAssetModelByCodeCommand

Representa la solicitud para buscar un modelo
de activo mediante su código.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class FindAssetModelByCodeCommand:
    """
    Contiene la información necesaria para buscar
    un modelo de activo.
    """

    code: str
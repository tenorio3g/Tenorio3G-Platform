"""
T3G-ASSET-UC-003

FindAllAssetModelsCommand

Este caso de uso no requiere parámetros,
pero mantenemos el Command para conservar
la misma arquitectura en todos los casos de uso.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class FindAllAssetModelsCommand:
    """
    Solicitud para obtener todos los modelos
    de activos registrados.
    """
    pass
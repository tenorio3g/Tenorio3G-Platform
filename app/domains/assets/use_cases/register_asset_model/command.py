"""
T3G-ASSET-UC-001

RegisterAssetModelCommand

Objeto que transporta la información necesaria para registrar
un nuevo modelo de activo.
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class RegisterAssetModelCommand:
    """
    Datos necesarios para registrar un modelo de activo.
    """

    code: str
    name: str
    model_number: str
    manufacturer_code: str
    asset_type_code: str
    description: str = ""
    specifications: dict[str, str] = field(default_factory=dict)
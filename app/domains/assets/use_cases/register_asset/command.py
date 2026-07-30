from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


@dataclass(slots=True)
class RegisterAssetCommand:
    """
    Datos necesarios para registrar un activo físico.
    """

    code: str
    name: str
    asset_model_code: str
    serial_number: str
    location_code: str
    status: AssetStatus
    installation_date: date
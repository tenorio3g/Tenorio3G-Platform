from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.domains.assets.value_objects.asset_status import AssetStatus


@dataclass(slots=True, frozen=True)
class UpdateAssetCommand:
    """
    Datos permitidos para actualizar un activo.

    El codigo identifica al activo y no puede modificarse.
    Los campos con valor None conservaran su valor actual.
    """

    code: str
    name: str | None = None
    asset_model_code: str | None = None
    serial_number: str | None = None
    location_code: str | None = None
    installation_date: date | None = None
    status: AssetStatus | None = None

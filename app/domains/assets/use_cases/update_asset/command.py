from __future__ import annotations

from dataclasses import dataclass

from app.domains.assets.value_objects.asset_status import AssetStatus


@dataclass(slots=True, frozen=True)
class UpdateAssetCommand:
    """
    Datos permitidos para actualizar un activo.

    El código identifica al activo y no puede modificarse.
    Los campos con valor None conservarán su valor actual.
    """

    code: str
    name: str | None = None
    serial_number: str | None = None
    location_code: str | None = None
    status: AssetStatus | None = None
from __future__ import annotations

from enum import Enum


class AssetStatus(str, Enum):
    """
    Estados operativos permitidos para un activo.
    """

    OPERATING = "OPERATING"

    STOPPED = "STOPPED"

    MAINTENANCE = "MAINTENANCE"

    OUT_OF_SERVICE = "OUT_OF_SERVICE"

    RETIRED = "RETIRED"
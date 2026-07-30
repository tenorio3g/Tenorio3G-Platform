from __future__ import annotations

from datetime import date

from app.domains.assets.value_objects.asset_status import AssetStatus


class Asset:
    """
    Entidad principal del dominio Assets.

    Representa un activo físico dentro de la organización.
    """

    def __init__(
        self,
        code: str,
        name: str,
        asset_model_code: str,
        serial_number: str,
        location_code: str,
        status: AssetStatus,
        installation_date: date,
        deactivation_reason: str | None = None,
    ) -> None:

        self.code = code
        self.name = name
        self.asset_model_code = asset_model_code
        self.serial_number = serial_number
        self.location_code = location_code
        self.status = status
        self.installation_date = installation_date
        self.deactivation_reason = deactivation_reason

    # ==========================================================
    # Consultas
    # ==========================================================

    def is_operating(self) -> bool:
        """
        Indica si el activo se encuentra operando.
        """
        return self.status == AssetStatus.OPERATING

    def is_out_of_service(self) -> bool:
        """
        Indica si el activo está fuera de servicio.
        """
        return self.status == AssetStatus.OUT_OF_SERVICE

    # ==========================================================
    # Cambios de información
    # ==========================================================

    def rename(
        self,
        new_name: str,
    ) -> None:

        self.name = new_name.strip()

    def change_serial_number(
        self,
        serial_number: str,
    ) -> None:

        self.serial_number = serial_number.strip()

    def change_location(
        self,
        location_code: str,
    ) -> None:

        self.location_code = location_code.strip()

    def change_status(
        self,
        status: AssetStatus,
    ) -> None:

        self.status = status

    # ==========================================================
    # Ciclo de vida
    # ==========================================================

    def activate(self) -> None:
        """
        Activa nuevamente el activo.
        """

        self.status = AssetStatus.OPERATING
        self.deactivation_reason = None

    def deactivate(
        self,
        reason: str,
    ) -> None:
        """
        Coloca el activo fuera de servicio.
        """

        clean_reason = reason.strip()

        if not clean_reason:
            raise ValueError(
                "El motivo de desactivación es obligatorio."
            )

        self.status = AssetStatus.OUT_OF_SERVICE
        self.deactivation_reason = clean_reason

    # ==========================================================
    # Representación
    # ==========================================================

    def __repr__(self) -> str:

        return (
            f"Asset("
            f"code='{self.code}', "
            f"name='{self.name}', "
            f"status='{self.status.name}')"
        )
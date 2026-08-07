from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)
from app.domains.assets.technical_data.repositories.technical_data_repository import (
    TechnicalDataRepository,
)

from .command import SaveTechnicalDataCommand
from .result import SaveTechnicalDataResult


class SaveTechnicalData:
    """
    Crea o actualiza la ficha técnica de un activo.
    """

    def __init__(
        self,
        repository: TechnicalDataRepository,
    ) -> None:
        self._repository = repository

    def execute(
        self,
        command: SaveTechnicalDataCommand,
    ) -> SaveTechnicalDataResult:

        asset_code = command.asset_code.strip()
        equipment_type = command.equipment_type.strip()

        if not asset_code:
            return SaveTechnicalDataResult(
                success=False,
                message="El código del activo es obligatorio.",
            )

        if not equipment_type:
            return SaveTechnicalDataResult(
                success=False,
                message="El tipo de equipo es obligatorio.",
            )

        technical_data = TechnicalData(
            asset_code=asset_code,
            equipment_type=equipment_type,
            manufacturer=command.manufacturer.strip(),
            model=command.model.strip(),
            serial_number=command.serial_number.strip(),
            voltage=command.voltage.strip(),
            phases=command.phases.strip(),
            frequency=command.frequency.strip(),
            motor_power=command.motor_power.strip(),
            observations=command.observations.strip(),
        )

        self._repository.save(technical_data)

        return SaveTechnicalDataResult(
            success=True,
            message="Datos técnicos guardados correctamente.",
        )
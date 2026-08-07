from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)

from .technical_data_view_model import (
    TechnicalDataViewModel,
)


class TechnicalDataPresenter:
    """
    Adapta los datos técnicos del dominio para la interfaz.
    """

    @staticmethod
    def present(
        technical_data: TechnicalData,
    ) -> TechnicalDataViewModel:

        return TechnicalDataViewModel(
            equipment_type=(
                technical_data.equipment_type
                or "Sin tipo registrado"
            ),
            manufacturer=(
                technical_data.manufacturer
                or "Sin fabricante registrado"
            ),
            model=(
                technical_data.model
                or "Sin modelo registrado"
            ),
            serial_number=(
                technical_data.serial_number
                or "Sin número de serie"
            ),
            voltage=(
                technical_data.voltage
                or "Sin voltaje registrado"
            ),
            phases=(
                technical_data.phases
                or "Sin fases registradas"
            ),
            frequency=(
                technical_data.frequency
                or "Sin frecuencia registrada"
            ),
            motor_power=(
                technical_data.motor_power
                or "No aplica / sin registrar"
            ),
            observations=(
                technical_data.observations
                or "Sin observaciones técnicas."
            ),
        )
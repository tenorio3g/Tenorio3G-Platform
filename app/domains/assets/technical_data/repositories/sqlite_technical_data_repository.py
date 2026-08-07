from __future__ import annotations

from sqlalchemy import select

from app.foundation.database import SessionLocal

from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)
from app.domains.assets.technical_data.models.technical_data_model import (
    TechnicalDataModel,
)
from app.domains.assets.technical_data.repositories.technical_data_repository import (
    TechnicalDataRepository,
)


class SQLiteTechnicalDataRepository(
    TechnicalDataRepository,
):
    """
    Implementación SQLite del repositorio de datos técnicos.

    Traduce entre la entidad de dominio TechnicalData
    y el modelo ORM TechnicalDataModel.
    """

    def get_by_asset_code(
        self,
        asset_code: str,
    ) -> TechnicalData | None:

        clean_code = asset_code.strip()

        if not clean_code:
            return None

        with SessionLocal() as session:

            statement = select(
                TechnicalDataModel
            ).where(
                TechnicalDataModel.asset_code
                == clean_code
            )

            model = session.scalar(statement)

            if model is None:
                return None

            return self._to_entity(model)

    def save(
        self,
        technical_data: TechnicalData,
    ) -> None:

        clean_code = technical_data.asset_code.strip()

        if not clean_code:
            raise ValueError(
                "El código del activo es obligatorio."
            )

        with SessionLocal() as session:

            statement = select(
                TechnicalDataModel
            ).where(
                TechnicalDataModel.asset_code
                == clean_code
            )

            model = session.scalar(statement)

            if model is None:

                model = self._to_model(
                    technical_data,
                )

                session.add(model)

            else:

                self._update_model(
                    model=model,
                    technical_data=technical_data,
                )

            session.commit()

    @staticmethod
    def _to_entity(
        model: TechnicalDataModel,
    ) -> TechnicalData:
        """
        Convierte el modelo ORM en entidad de dominio.
        """

        return TechnicalData(
            asset_code=model.asset_code,
            equipment_type=model.equipment_type,
            manufacturer=model.manufacturer,
            model=model.model,
            serial_number=model.serial_number,
            voltage=model.voltage,
            phases=model.phases,
            frequency=model.frequency,
            motor_power=model.motor_power,
            observations=model.observations,
        )

    @staticmethod
    def _to_model(
        technical_data: TechnicalData,
    ) -> TechnicalDataModel:
        """
        Convierte la entidad de dominio en modelo ORM.
        """

        return TechnicalDataModel(
            asset_code=technical_data.asset_code.strip(),
            equipment_type=technical_data.equipment_type,
            manufacturer=technical_data.manufacturer,
            model=technical_data.model,
            serial_number=technical_data.serial_number,
            voltage=technical_data.voltage,
            phases=technical_data.phases,
            frequency=technical_data.frequency,
            motor_power=technical_data.motor_power,
            observations=technical_data.observations,
        )

    @staticmethod
    def _update_model(
        model: TechnicalDataModel,
        technical_data: TechnicalData,
    ) -> None:
        """
        Actualiza un registro ORM existente.
        """

        model.equipment_type = (
            technical_data.equipment_type
        )
        model.manufacturer = (
            technical_data.manufacturer
        )
        model.model = technical_data.model
        model.serial_number = (
            technical_data.serial_number
        )
        model.voltage = technical_data.voltage
        model.phases = technical_data.phases
        model.frequency = technical_data.frequency
        model.motor_power = (
            technical_data.motor_power
        )
        model.observations = (
            technical_data.observations
        )
from app.foundation.database import Base, engine

from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)

from app.domains.assets.technical_data.models.technical_data_model import (
    TechnicalDataModel,
)

from app.domains.assets.technical_data.bootstrap import (
    technical_data_repository,
)


def main() -> None:

    Base.metadata.create_all(engine)

    technical_data_repository.save(
        TechnicalData(
            asset_code="S2-480-ES09-T269",
            equipment_type="Tablero eléctrico general",
            manufacturer="Sin registrar",
            model="TAB-480-01",
            serial_number="Sin registrar",
            voltage="480 V",
            phases="3",
            frequency="60 Hz",
            motor_power="No aplica",
            observations=(
                "Tablero general ubicado en "
                "Subestación Norte."
            ),
        )
    )

    print(
        "Datos técnicos de ES09 registrados correctamente."
    )


if __name__ == "__main__":
    main()
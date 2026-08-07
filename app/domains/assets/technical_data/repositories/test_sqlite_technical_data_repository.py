from __future__ import annotations

from app.foundation.database import Base, engine

from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)
from app.domains.assets.technical_data.models.technical_data_model import (
    TechnicalDataModel,
)
from app.domains.assets.technical_data.repositories.sqlite_technical_data_repository import (
    SQLiteTechnicalDataRepository,
)


def test_should_save_and_get_technical_data() -> None:

    # La importación de TechnicalDataModel registra
    # la tabla dentro de Base.metadata.
    assert TechnicalDataModel.__tablename__ == (
        "asset_technical_data"
    )

    Base.metadata.create_all(engine)

    repository = SQLiteTechnicalDataRepository()

    technical_data = TechnicalData(
        asset_code="TEST-AHA-24",
        equipment_type="Manejadora de aire",
        manufacturer="Sin registrar",
        model="Sin registrar",
        serial_number="Sin registrar",
        voltage="480 V",
        phases="3",
        frequency="60 Hz",
        motor_power="15 HP",
        observations=(
            "Registro temporal para prueba "
            "de persistencia."
        ),
    )

    repository.save(technical_data)

    persisted = repository.get_by_asset_code(
        "TEST-AHA-24",
    )

    assert persisted is not None
    assert persisted.asset_code == "TEST-AHA-24"
    assert persisted.equipment_type == (
        "Manejadora de aire"
    )
    assert persisted.voltage == "480 V"
    assert persisted.phases == "3"
    assert persisted.motor_power == "15 HP"
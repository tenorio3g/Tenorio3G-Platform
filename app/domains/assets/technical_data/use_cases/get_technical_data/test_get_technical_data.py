from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)
from app.domains.assets.technical_data.repositories.in_memory_technical_data_repository import (
    InMemoryTechnicalDataRepository,
)
from app.domains.assets.technical_data.use_cases.get_technical_data import (
    GetTechnicalData,
    GetTechnicalDataQuery,
)


def test_should_get_technical_data() -> None:

    repository = InMemoryTechnicalDataRepository()

    repository.save(
        TechnicalData(
            asset_code="AHA-24",
            equipment_type="Manejadora de aire",
            manufacturer="Sin registrar",
            model="Sin registrar",
            serial_number="Sin registrar",
            voltage="480 V",
            phases="3",
            frequency="60 Hz",
            motor_power="15 HP",
            observations=(
                "Verificar bandas y baleros "
                "durante el mantenimiento."
            ),
        )
    )

    use_case = GetTechnicalData(repository)

    result = use_case.execute(
        GetTechnicalDataQuery(
            asset_code="AHA-24",
        )
    )

    assert result.success is True
    assert result.technical_data is not None
    assert result.technical_data.asset_code == "AHA-24"
    assert result.technical_data.voltage == "480 V"


def test_should_fail_when_technical_data_does_not_exist() -> None:

    repository = InMemoryTechnicalDataRepository()

    use_case = GetTechnicalData(repository)

    result = use_case.execute(
        GetTechnicalDataQuery(
            asset_code="UNKNOWN",
        )
    )

    assert result.success is False
    assert result.technical_data is None
    assert result.message == (
        "No existe información técnica para este activo."
    )
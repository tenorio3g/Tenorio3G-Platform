from app.domains.assets.technical_data.repositories.in_memory_technical_data_repository import (
    InMemoryTechnicalDataRepository,
)
from app.domains.assets.technical_data.use_cases.save_technical_data import (
    SaveTechnicalData,
    SaveTechnicalDataCommand,
)


def test_should_save_technical_data() -> None:
    repository = InMemoryTechnicalDataRepository()
    use_case = SaveTechnicalData(repository)

    result = use_case.execute(
        SaveTechnicalDataCommand(
            asset_code="AHA-24",
            equipment_type="Manejadora de aire",
            manufacturer="Trane",
            model="Sin registrar",
            serial_number="Sin registrar",
            voltage="480 V",
            phases="3",
            frequency="60 Hz",
            motor_power="15 HP",
            observations="Equipo de prueba.",
        )
    )

    persisted = repository.get_by_asset_code("AHA-24")

    assert result.success is True
    assert persisted is not None
    assert persisted.manufacturer == "Trane"
    assert persisted.voltage == "480 V"


def test_should_fail_without_equipment_type() -> None:
    repository = InMemoryTechnicalDataRepository()
    use_case = SaveTechnicalData(repository)

    result = use_case.execute(
        SaveTechnicalDataCommand(
            asset_code="AHA-24",
            equipment_type="",
            manufacturer="Trane",
            model="",
            serial_number="",
            voltage="480 V",
            phases="3",
            frequency="60 Hz",
            motor_power="15 HP",
            observations="",
        )
    )

    assert result.success is False
    assert result.message == (
        "El tipo de equipo es obligatorio."
    )
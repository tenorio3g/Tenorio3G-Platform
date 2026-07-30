"""
T3G-ASSET-UC-001

Pruebas unitarias para el caso de uso RegisterAssetModel.
"""

from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)
from app.domains.assets.use_cases.register_asset_model.command import (
    RegisterAssetModelCommand,
)
from app.domains.assets.use_cases.register_asset_model.register_asset_model import (
    RegisterAssetModel,
)


def test_register_asset_model_success() -> None:
    """
    Verifica que un modelo válido pueda registrarse correctamente.
    """

    repository = InMemoryAssetModelRepository()
    use_case = RegisterAssetModel(repository)

    command = RegisterAssetModelCommand(
        code="30XA120",
        name="30XA Air Cooled Chiller",
        model_number="30XA-120",
        manufacturer_code="CARRIER",
        asset_type_code="HVAC",
        description="Chiller Carrier enfriado por aire.",
        specifications={
            "voltage": "480 VAC",
            "frequency": "60 Hz",
        },
    )

    result = use_case.execute(command)

    assert result.success is True
    assert result.message == "Modelo registrado correctamente."
    assert result.asset_model is not None

    assert result.asset_model.code == "30XA120"
    assert result.asset_model.name == "30XA Air Cooled Chiller"
    assert result.asset_model.model_number == "30XA-120"
    assert result.asset_model.manufacturer_code == "CARRIER"
    assert result.asset_model.asset_type_code == "HVAC"

    assert repository.exists_by_code("30XA120") is True

    saved_model = repository.find_by_code("30XA120")

    assert saved_model is not None
    assert saved_model.code == "30XA120"


def test_duplicate_asset_model_code_returns_error() -> None:
    """
    Verifica que no se permita registrar dos modelos
    con el mismo código.
    """

    repository = InMemoryAssetModelRepository()
    use_case = RegisterAssetModel(repository)

    command = RegisterAssetModelCommand(
        code="30XA120",
        name="30XA Air Cooled Chiller",
        model_number="30XA-120",
        manufacturer_code="CARRIER",
        asset_type_code="HVAC",
    )

    first_result = use_case.execute(command)
    second_result = use_case.execute(command)

    assert first_result.success is True

    assert second_result.success is False
    assert second_result.asset_model is None
    assert second_result.message == (
        "Ya existe un modelo con el código '30XA120'."
    )

    assert len(repository.find_all()) == 1
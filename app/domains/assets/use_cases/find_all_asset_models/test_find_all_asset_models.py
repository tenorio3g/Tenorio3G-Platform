"""
T3G-ASSET-UC-003

Pruebas unitarias para FindAllAssetModels.
"""

from app.domains.assets.entities.asset_model import AssetModel
from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)

from app.domains.assets.use_cases.find_all_asset_models.command import (
    FindAllAssetModelsCommand,
)

from app.domains.assets.use_cases.find_all_asset_models.find_all_asset_models import (
    FindAllAssetModels,
)


def test_find_all_asset_models_returns_registered_models() -> None:
    """
    Debe devolver todos los modelos registrados.
    """

    repository = InMemoryAssetModelRepository()

    first_model = AssetModel(
        code="30XA120",
        name="30XA Air Cooled Chiller",
        model_number="30XA-120",
        manufacturer_code="CARRIER",
        asset_type_code="HVAC",
        description="Chiller Carrier",
        specifications={
            "voltage": "480 VAC",
        },
    )

    second_model = AssetModel(
        code="YZD250",
        name="YZD Centrifugal Chiller",
        model_number="YZD-250",
        manufacturer_code="YORK",
        asset_type_code="HVAC",
        description="Chiller centrífugo York",
        specifications={
            "voltage": "480 VAC",
        },
    )

    repository.save(first_model)
    repository.save(second_model)

    use_case = FindAllAssetModels(repository)

    command = FindAllAssetModelsCommand()

    result = use_case.execute(command)

    assert result.success is True
    assert result.message == "Modelos obtenidos correctamente."
    assert len(result.asset_models) == 2

    assert result.asset_models[0].code == "30XA120"
    assert result.asset_models[1].code == "YZD250"


def test_find_all_asset_models_returns_empty_list() -> None:
    """
    Debe devolver una lista vacía cuando no existan modelos.
    """

    repository = InMemoryAssetModelRepository()

    use_case = FindAllAssetModels(repository)

    command = FindAllAssetModelsCommand()

    result = use_case.execute(command)

    assert result.success is True
    assert result.message == "Modelos obtenidos correctamente."
    assert result.asset_models == []
    assert len(result.asset_models) == 0
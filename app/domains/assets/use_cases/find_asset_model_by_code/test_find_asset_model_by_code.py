"""
T3G-ASSET-UC-002

Pruebas unitarias para FindAssetModelByCode.
"""

from app.domains.assets.entities.asset_model import AssetModel
from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)

from app.domains.assets.use_cases.find_asset_model_by_code.command import (
    FindAssetModelByCodeCommand,
)

from app.domains.assets.use_cases.find_asset_model_by_code.find_asset_model_by_code import (
    FindAssetModelByCode,
)


def test_find_existing_asset_model() -> None:
    """
    Debe encontrar un modelo previamente registrado.
    """

    repository = InMemoryAssetModelRepository()

    asset_model = AssetModel(
        code="30XA120",
        name="30XA Air Cooled Chiller",
        model_number="30XA-120",
        manufacturer_code="CARRIER",
        asset_type_code="HVAC",
        description="Chiller Carrier",
        specifications={},
    )

    repository.save(asset_model)

    use_case = FindAssetModelByCode(repository)

    command = FindAssetModelByCodeCommand(
        code="30XA120",
    )

    result = use_case.execute(command)

    assert result.success is True
    assert result.asset_model is not None
    assert result.asset_model.code == "30XA120"


def test_find_non_existing_asset_model() -> None:
    """
    Debe indicar que el modelo no existe.
    """

    repository = InMemoryAssetModelRepository()

    use_case = FindAssetModelByCode(repository)

    command = FindAssetModelByCodeCommand(
        code="NO_EXISTE",
    )

    result = use_case.execute(command)

    assert result.success is False
    assert result.asset_model is None
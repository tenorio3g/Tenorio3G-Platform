from app.domains.assets.entities.asset_model import AssetModel
from app.domains.assets.repositories.in_memory_asset_model_repository import (
    InMemoryAssetModelRepository,
)

from .command import UpdateAssetModelCommand
from .update_asset_model import UpdateAssetModel


def test_should_update_asset_model_successfully():

    repository = InMemoryAssetModelRepository()

    asset_model = AssetModel(
        code="CHILLER240",
        name="Carrier Chiller",
        model_number="30XA-240",
        manufacturer_code="CARRIER",
        asset_type_code="CHILLER",
        description="Descripción anterior",
        specifications={
            "voltaje": "480 V",
        },
    )

    repository.save(asset_model)

    command = UpdateAssetModelCommand(
        code="CHILLER240",
        name="Carrier Chiller Actualizado",
        description="Nueva descripción",
        specifications={
            "voltaje": "460 V",
            "frecuencia": "60 Hz",
        },
    )

    use_case = UpdateAssetModel(repository)

    result = use_case.execute(command)

    assert result.success is True
    assert result.asset_model is not None
    assert result.asset_model.name == "Carrier Chiller Actualizado"
    assert result.asset_model.description == "Nueva descripción"
    assert result.asset_model.specifications == {
        "voltaje": "460 V",
        "frecuencia": "60 Hz",
    }


def test_should_fail_when_asset_model_does_not_exist():

    repository = InMemoryAssetModelRepository()

    command = UpdateAssetModelCommand(
        code="UNKNOWN",
        name="Nuevo Nombre",
        description="Descripción",
        specifications={},
    )

    use_case = UpdateAssetModel(repository)

    result = use_case.execute(command)

    assert result.success is False
    assert result.asset_model is None
    assert result.message == "No existe un modelo con ese código."
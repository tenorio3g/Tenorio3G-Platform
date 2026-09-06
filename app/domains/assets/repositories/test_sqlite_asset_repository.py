from datetime import date

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.entities.asset import Asset

from app.domains.assets.models import (
    AssetRecordModel,
)

from app.domains.assets.repositories import (
    SQLiteAssetRepository,
)

from app.domains.assets.value_objects.asset_status import (
    AssetStatus,
)


@pytest.fixture
def repository(tmp_path):

    database_path = (
        tmp_path / "assets_test.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path.as_posix()}",
        future=True,
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(engine)

    repository = SQLiteAssetRepository(
        SessionLocal
    )

    yield repository

    Base.metadata.drop_all(engine)
    engine.dispose()


def create_asset(
    code="CH-001",
    name="Chiller Principal",
    asset_model_code="CHILLER240",
    serial_number="SN-987654",
    location_code="PLANTA_NORTE",
    status=AssetStatus.OPERATING,
    installation_date=date(2025, 1, 15),
    deactivation_reason=None,
):
    return Asset(
        code=code,
        name=name,
        asset_model_code=asset_model_code,
        serial_number=serial_number,
        location_code=location_code,
        status=status,
        installation_date=installation_date,
        deactivation_reason=deactivation_reason,
    )


def test_should_save_and_find_asset(
    repository,
):
    repository.save(
        create_asset()
    )

    asset = repository.find_by_code(
        "CH-001"
    )

    assert asset is not None
    assert asset.code == "CH-001"
    assert asset.name == "Chiller Principal"
    assert asset.asset_model_code == "CHILLER240"
    assert asset.serial_number == "SN-987654"
    assert asset.location_code == "PLANTA_NORTE"
    assert asset.status == AssetStatus.OPERATING
    assert asset.installation_date == date(
        2025,
        1,
        15,
    )
    assert asset.deactivation_reason is None


def test_should_persist_asset_between_sessions(
    repository,
):
    repository.save(
        create_asset()
    )

    asset = repository.find_by_code(
        "CH-001"
    )

    assert asset is not None
    assert asset.name == "Chiller Principal"


def test_should_return_none_when_asset_does_not_exist(
    repository,
):
    asset = repository.find_by_code(
        "UNKNOWN"
    )

    assert asset is None


def test_should_list_all_assets_ordered_by_code(
    repository,
):
    repository.save(
        create_asset(
            code="CH-002",
            name="Chiller Secundario",
        )
    )

    repository.save(
        create_asset(
            code="CH-001",
            name="Chiller Principal",
        )
    )

    assets = repository.find_all()

    assert [
        asset.code
        for asset in assets
    ] == [
        "CH-001",
        "CH-002",
    ]


def test_should_update_existing_asset(
    repository,
):
    asset = create_asset()

    repository.save(asset)

    asset.rename(
        "Chiller Principal Actualizado"
    )

    asset.change_serial_number(
        "SN-UPDATED"
    )

    asset.change_location(
        "PLANTA_SUR"
    )

    repository.update(asset)

    persisted = repository.find_by_code(
        "CH-001"
    )

    assert persisted is not None
    assert (
        persisted.name
        == "Chiller Principal Actualizado"
    )
    assert persisted.serial_number == "SN-UPDATED"
    assert persisted.location_code == "PLANTA_SUR"


def test_should_persist_deactivation_reason(
    repository,
):
    asset = create_asset()

    repository.save(asset)

    asset.deactivate(
        "Equipo fuera de servicio por mantenimiento."
    )

    repository.update(asset)

    persisted = repository.find_by_code(
        "CH-001"
    )

    assert persisted is not None
    assert (
        persisted.status
        == AssetStatus.OUT_OF_SERVICE
    )
    assert (
        persisted.deactivation_reason
        == "Equipo fuera de servicio por mantenimiento."
    )


def test_should_not_create_asset_when_updating_unknown_asset(
    repository,
):
    asset = create_asset(
        code="UNKNOWN"
    )

    repository.update(asset)

    persisted = repository.find_by_code(
        "UNKNOWN"
    )

    assert persisted is None
def test_should_save_asset_without_installation_date(
    repository,
):
    asset = create_asset(
        code="ASSET-NO-INSTALL-DATE",
        installation_date=None,
    )

    repository.save(asset)

    stored_asset = repository.find_by_code(
        "ASSET-NO-INSTALL-DATE"
    )

    assert stored_asset is not None
    assert stored_asset.installation_date is None

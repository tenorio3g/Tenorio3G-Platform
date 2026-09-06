import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.assets.entities.asset_model import (
    AssetModel,
)
from app.domains.assets.models import (
    AssetModelRecord,
)
from app.domains.assets.repositories import (
    SQLiteAssetModelRepository,
)


@pytest.fixture
def repository(tmp_path):

    database_path = (
        tmp_path / "asset_models_test.db"
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

    repository = SQLiteAssetModelRepository(
        SessionLocal
    )

    yield repository

    Base.metadata.drop_all(engine)
    engine.dispose()


def create_asset_model(
    code="30XA120",
    name="30XA Air Cooled Chiller",
):
    return AssetModel(
        code=code,
        name=name,
        model_number="30XA-120",
        asset_type_code="HVAC",
        manufacturer_code="CARRIER",
        description=(
            "Chiller Carrier enfriado por aire."
        ),
        aliases=(
            "30XA",
            "AquaForce",
        ),
        specifications={
            "voltage": "480 VAC",
            "frequency": "60 Hz",
        },
    )


def test_should_save_and_find_asset_model(
    repository,
):
    repository.save(
        create_asset_model()
    )

    model = repository.find_by_code(
        "30XA120"
    )

    assert model is not None
    assert model.code == "30XA120"
    assert model.name == "30XA Air Cooled Chiller"
    assert model.model_number == "30XA-120"
    assert model.asset_type_code == "HVAC"
    assert model.manufacturer_code == "CARRIER"
    assert (
        model.description
        == "Chiller Carrier enfriado por aire."
    )
    assert model.aliases == (
        "30XA",
        "AquaForce",
    )
    assert model.specifications == {
        "voltage": "480 VAC",
        "frequency": "60 Hz",
    }
    assert model.is_active is True
    assert model.is_obsolete is False


def test_should_find_code_case_insensitively(
    repository,
):
    repository.save(
        create_asset_model()
    )

    model = repository.find_by_code(
        "  30xa120  "
    )

    assert model is not None
    assert model.code == "30XA120"


def test_should_report_existing_asset_model(
    repository,
):
    repository.save(
        create_asset_model()
    )

    assert repository.exists_by_code(
        "30xa120"
    ) is True

    assert repository.exists_by_code(
        "UNKNOWN"
    ) is False


def test_should_list_all_asset_models_ordered_by_code(
    repository,
):
    repository.save(
        create_asset_model(
            code="MODEL-B",
            name="Model B",
        )
    )

    repository.save(
        create_asset_model(
            code="MODEL-A",
            name="Model A",
        )
    )

    models = repository.find_all()

    assert [
        model.code
        for model in models
    ] == [
        "MODEL-A",
        "MODEL-B",
    ]


def test_should_update_asset_model(
    repository,
):
    asset_model = create_asset_model()

    repository.save(asset_model)

    asset_model.rename(
        "30XA Updated"
    )
    asset_model.change_description(
        "Descripci?n actualizada."
    )
    asset_model.add_alias(
        "Carrier Chiller"
    )
    asset_model.set_specification(
        "capacity",
        "120 TR",
    )
    asset_model.mark_as_obsolete()
    asset_model.deactivate()

    repository.update(
        asset_model
    )

    persisted = repository.find_by_code(
        "30XA120"
    )

    assert persisted is not None
    assert persisted.name == "30XA Updated"
    assert (
        persisted.description
        == "Descripci?n actualizada."
    )
    assert "Carrier Chiller" in persisted.aliases
    assert (
        persisted.specifications["capacity"]
        == "120 TR"
    )
    assert persisted.is_obsolete is True
    assert persisted.is_active is False


def test_should_not_create_model_when_updating_unknown_model(
    repository,
):
    asset_model = create_asset_model(
        code="UNKNOWN"
    )

    repository.update(
        asset_model
    )

    assert repository.find_by_code(
        "UNKNOWN"
    ) is None


def test_should_delete_asset_model(
    repository,
):
    repository.save(
        create_asset_model()
    )

    repository.delete_by_code(
        "30xa120"
    )

    assert repository.find_by_code(
        "30XA120"
    ) is None

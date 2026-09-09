from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base
from app.maps.models.map_layer import MapLayer
from app.maps.repositories.sqlite_map_layer_repository import (
    SQLiteMapLayerRepository,
)


def create_repository(tmp_path):
    database_path = (
        tmp_path
        / "map_layers_repository.db"
    )

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    TestSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    Base.metadata.create_all(
        bind=engine
    )

    repository = (
        SQLiteMapLayerRepository(
            TestSessionLocal
        )
    )

    return repository, engine


def create_layer(
    code,
    name,
    order,
    is_active=True,
):
    return MapLayer(
        code=code,
        name=name,
        order=order,
        is_active=is_active,
    )


def test_should_save_and_find_layer_by_code(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_layer(
            "electrical",
            "Electrico",
            10,
        )
    )

    layer = repository.find_by_code(
        "electrical"
    )

    assert layer is not None
    assert layer.code == "electrical"
    assert layer.name == "Electrico"
    assert layer.order == 10
    assert layer.is_active is True

    engine.dispose()


def test_find_by_code_should_normalize_input(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_layer(
            "electrical",
            "Electrico",
            10,
        )
    )

    layer = repository.find_by_code(
        "  ELECTRICAL  "
    )

    assert layer is not None
    assert layer.code == "electrical"

    engine.dispose()


def test_find_by_code_should_return_none_when_missing(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    assert (
        repository.find_by_code("missing")
        is None
    )

    engine.dispose()


def test_save_should_update_existing_layer(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_layer(
            "electrical",
            "Electrico",
            10,
            True,
        )
    )

    repository.save(
        create_layer(
            "electrical",
            "Sistema Electrico",
            20,
            False,
        )
    )

    layers = repository.find_all()

    assert len(layers) == 1
    assert layers[0].name == "Sistema Electrico"
    assert layers[0].order == 20
    assert layers[0].is_active is False

    engine.dispose()


def test_find_all_should_order_by_order_then_name(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_layer(
            "hvac",
            "HVAC",
            20,
        )
    )

    repository.save(
        create_layer(
            "lighting",
            "Iluminacion",
            10,
        )
    )

    repository.save(
        create_layer(
            "electrical",
            "Electrico",
            10,
        )
    )

    layers = repository.find_all()

    assert [
        layer.code
        for layer in layers
    ] == [
        "electrical",
        "lighting",
        "hvac",
    ]

    engine.dispose()


def test_find_active_should_exclude_inactive_layers(
    tmp_path,
):
    repository, engine = create_repository(
        tmp_path
    )

    repository.save(
        create_layer(
            "electrical",
            "Electrico",
            10,
            True,
        )
    )

    repository.save(
        create_layer(
            "hvac",
            "HVAC",
            20,
            False,
        )
    )

    layers = repository.find_active()

    assert [
        layer.code
        for layer in layers
    ] == [
        "electrical",
    ]

    engine.dispose()

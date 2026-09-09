from app.maps.models.map_layer import MapLayer
from app.maps.repositories.in_memory_map_layer_repository import (
    InMemoryMapLayerRepository,
)


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


def test_repository_should_save_and_find_layer_by_code():
    repository = InMemoryMapLayerRepository()

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


def test_find_by_code_should_normalize_input():
    repository = InMemoryMapLayerRepository()

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


def test_find_by_code_should_return_none_when_missing():
    repository = InMemoryMapLayerRepository()

    assert (
        repository.find_by_code("missing")
        is None
    )


def test_save_should_replace_existing_layer():
    repository = InMemoryMapLayerRepository()

    repository.save(
        create_layer(
            "electrical",
            "Electrico",
            10,
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


def test_find_all_should_order_by_order_then_name():
    repository = InMemoryMapLayerRepository()

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


def test_find_active_should_exclude_inactive_layers():
    repository = InMemoryMapLayerRepository()

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

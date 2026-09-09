from app.maps.models.map_layer import MapLayer
from app.maps.repositories.in_memory_map_layer_repository import (
    InMemoryMapLayerRepository,
)
from app.maps.use_cases.ensure_default_map_layers import (
    EnsureDefaultMapLayers,
)


def test_should_create_default_layers():
    repository = InMemoryMapLayerRepository()

    use_case = EnsureDefaultMapLayers(
        repository
    )

    result = use_case.execute()

    assert result.success is True

    layers = repository.find_all()

    assert [
        layer.code
        for layer in layers
    ] == [
        "electrical",
        "hvac",
    ]

    assert layers[0].name == "Electrico"
    assert layers[0].order == 10
    assert layers[0].is_active is True

    assert layers[1].name == "HVAC"
    assert layers[1].order == 20
    assert layers[1].is_active is True


def test_should_be_idempotent():
    repository = InMemoryMapLayerRepository()

    use_case = EnsureDefaultMapLayers(
        repository
    )

    use_case.execute()
    use_case.execute()

    layers = repository.find_all()

    assert len(layers) == 2

    assert [
        layer.code
        for layer in layers
    ] == [
        "electrical",
        "hvac",
    ]


def test_should_preserve_existing_layer_configuration():
    repository = InMemoryMapLayerRepository()

    repository.save(
        MapLayer(
            code="electrical",
            name="Electricidad Planta",
            order=5,
            is_active=False,
        )
    )

    use_case = EnsureDefaultMapLayers(
        repository
    )

    result = use_case.execute()

    assert result.success is True

    electrical = repository.find_by_code(
        "electrical"
    )

    assert electrical is not None
    assert electrical.name == "Electricidad Planta"
    assert electrical.order == 5
    assert electrical.is_active is False

    hvac = repository.find_by_code(
        "hvac"
    )

    assert hvac is not None
    assert hvac.name == "HVAC"

from app.maps.models.map_layer import MapLayer
from app.maps.repositories.in_memory_map_layer_repository import (
    InMemoryMapLayerRepository,
)
from app.maps.use_cases.list_active_map_layers import (
    ListActiveMapLayers,
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


def test_should_return_only_active_layers():
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
            True,
        )
    )

    repository.save(
        create_layer(
            "obsolete",
            "Obsoleta",
            30,
            False,
        )
    )

    use_case = ListActiveMapLayers(
        repository
    )

    result = use_case.execute()

    assert result.success is True

    assert [
        layer.code
        for layer in result.layers
    ] == [
        "electrical",
        "hvac",
    ]


def test_should_return_empty_result_when_no_active_layers():
    repository = InMemoryMapLayerRepository()

    repository.save(
        create_layer(
            "inactive",
            "Inactiva",
            10,
            False,
        )
    )

    use_case = ListActiveMapLayers(
        repository
    )

    result = use_case.execute()

    assert result.success is True
    assert result.layers == []


def test_should_preserve_repository_order():
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

    use_case = ListActiveMapLayers(
        repository
    )

    result = use_case.execute()

    assert [
        layer.code
        for layer in result.layers
    ] == [
        "electrical",
        "lighting",
        "hvac",
    ]

import pytest

from app.maps.models.map_layer import MapLayer


def test_map_layer_should_keep_valid_data():
    layer = MapLayer(
        code="electrical",
        name="Electrico",
        order=10,
        is_active=True,
    )

    assert layer.code == "electrical"
    assert layer.name == "Electrico"
    assert layer.order == 10
    assert layer.is_active is True


def test_map_layer_should_normalize_code_and_name():
    layer = MapLayer(
        code="  ELECTRICAL  ",
        name="  Electrico  ",
        order=10,
        is_active=True,
    )

    assert layer.code == "electrical"
    assert layer.name == "Electrico"


@pytest.mark.parametrize(
    ("code", "name"),
    [
        ("", "Electrico"),
        ("   ", "Electrico"),
        ("electrical", ""),
        ("electrical", "   "),
    ],
)
def test_map_layer_should_reject_empty_identity(
    code,
    name,
):
    with pytest.raises(ValueError):
        MapLayer(
            code=code,
            name=name,
            order=10,
            is_active=True,
        )


@pytest.mark.parametrize(
    "order",
    [
        -1,
        -10,
    ],
)
def test_map_layer_should_reject_negative_order(
    order,
):
    with pytest.raises(ValueError):
        MapLayer(
            code="electrical",
            name="Electrico",
            order=order,
            is_active=True,
        )


@pytest.mark.parametrize(
    "is_active",
    [
        1,
        0,
        "true",
        None,
    ],
)
def test_map_layer_should_require_boolean_active_state(
    is_active,
):
    with pytest.raises(ValueError):
        MapLayer(
            code="electrical",
            name="Electrico",
            order=10,
            is_active=is_active,
        )

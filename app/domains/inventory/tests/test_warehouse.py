import pytest

from app.domains.inventory.entities import (
    Warehouse,
)


def test_should_create_warehouse():

    warehouse = Warehouse(
        code="WH-001",
        name="Almacén de mantenimiento",
        description="Refacciones de mantenimiento.",
    )

    assert warehouse.code == "WH-001"
    assert (
        warehouse.name
        == "Almacén de mantenimiento"
    )
    assert (
        warehouse.description
        == "Refacciones de mantenimiento."
    )
    assert warehouse.is_active is True


def test_should_normalize_warehouse_code():

    warehouse = Warehouse(
        code=" wh-001 ",
        name="Almacén",
    )

    assert warehouse.code == "WH-001"


def test_should_trim_warehouse_name():

    warehouse = Warehouse(
        code="WH-001",
        name="  Almacén principal  ",
    )

    assert warehouse.name == "Almacén principal"


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_warehouse_code(
    code,
):

    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        Warehouse(
            code=code,
            name="Almacén",
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_warehouse_name(
    name,
):

    with pytest.raises(
        ValueError,
        match="name is required",
    ):
        Warehouse(
            code="WH-001",
            name=name,
        )


def test_should_reject_invalid_active_value():

    with pytest.raises(
        ValueError,
        match="is_active must be bool",
    ):
        Warehouse(
            code="WH-001",
            name="Almacén",
            is_active="YES",
        )


def test_should_deactivate_warehouse():

    warehouse = Warehouse(
        code="WH-001",
        name="Almacén",
    )

    warehouse.deactivate()

    assert warehouse.is_active is False


def test_should_activate_warehouse():

    warehouse = Warehouse(
        code="WH-001",
        name="Almacén",
        is_active=False,
    )

    warehouse.activate()

    assert warehouse.is_active is True

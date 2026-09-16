import pytest

from app.domains.inventory.entities import (
    InventoryLocation,
)


def test_should_create_inventory_location():

    location = InventoryLocation(
        code="LOC-001",
        warehouse_code="WH-001",
        name="Rack A - Nivel 2",
        aisle="A",
        rack="R01",
        level="02",
        bin="03",
        description="Refacciones mecánicas.",
    )

    assert location.code == "LOC-001"
    assert location.warehouse_code == "WH-001"
    assert location.name == "Rack A - Nivel 2"
    assert location.aisle == "A"
    assert location.rack == "R01"
    assert location.level == "02"
    assert location.bin == "03"
    assert (
        location.description
        == "Refacciones mecánicas."
    )
    assert location.is_active is True


def test_should_normalize_codes():

    location = InventoryLocation(
        code=" loc-001 ",
        warehouse_code=" wh-001 ",
        name="Ubicación",
    )

    assert location.code == "LOC-001"
    assert location.warehouse_code == "WH-001"


def test_should_trim_text_fields():

    location = InventoryLocation(
        code="LOC-001",
        warehouse_code="WH-001",
        name="  Ubicación principal  ",
        aisle=" A ",
        rack=" R01 ",
        level=" 02 ",
        bin=" 03 ",
        description="  Refacciones  ",
    )

    assert location.name == "Ubicación principal"
    assert location.aisle == "A"
    assert location.rack == "R01"
    assert location.level == "02"
    assert location.bin == "03"
    assert location.description == "Refacciones"


def test_should_allow_optional_location_fields():

    location = InventoryLocation(
        code="LOC-001",
        warehouse_code="WH-001",
        name="Área general",
    )

    assert location.aisle == ""
    assert location.rack == ""
    assert location.level == ""
    assert location.bin == ""
    assert location.description == ""


@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_location_code(
    code,
):

    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        InventoryLocation(
            code=code,
            warehouse_code="WH-001",
            name="Ubicación",
        )


@pytest.mark.parametrize(
    "warehouse_code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_warehouse_code(
    warehouse_code,
):

    with pytest.raises(
        ValueError,
        match="warehouse_code is required",
    ):
        InventoryLocation(
            code="LOC-001",
            warehouse_code=warehouse_code,
            name="Ubicación",
        )


@pytest.mark.parametrize(
    "name",
    [
        "",
        "   ",
    ],
)
def test_should_reject_empty_location_name(
    name,
):

    with pytest.raises(
        ValueError,
        match="name is required",
    ):
        InventoryLocation(
            code="LOC-001",
            warehouse_code="WH-001",
            name=name,
        )


def test_should_reject_invalid_active_value():

    with pytest.raises(
        ValueError,
        match="is_active must be bool",
    ):
        InventoryLocation(
            code="LOC-001",
            warehouse_code="WH-001",
            name="Ubicación",
            is_active="YES",
        )


def test_should_deactivate_location():

    location = InventoryLocation(
        code="LOC-001",
        warehouse_code="WH-001",
        name="Ubicación",
    )

    location.deactivate()

    assert location.is_active is False


def test_should_activate_location():

    location = InventoryLocation(
        code="LOC-001",
        warehouse_code="WH-001",
        name="Ubicación",
        is_active=False,
    )

    location.activate()

    assert location.is_active is True

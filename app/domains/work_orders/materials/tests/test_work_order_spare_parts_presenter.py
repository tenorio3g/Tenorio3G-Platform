from datetime import datetime

from app.domains.assets.spare_parts.entities import (
    SparePart,
)

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.presentation import (
    WorkOrderSparePartsPresenter,
)

from app.domains.work_orders.materials.use_cases import (
    ListWorkOrderSparePartsResult,
    WorkOrderSparePartItem,
)


def create_item(
    manufacturer="SKF",
    part_number="6204",
):

    spare_part = SparePart(
        code="SP-001",
        name="Rodamiento",
        manufacturer=manufacturer,
        part_number=part_number,
        unit="pieza",
    )

    usage = WorkOrderSparePartUsage(
        work_order_code="WO-001",
        spare_part_code="SP-001",
        quantity=2,
        unit_cost=15.5,
        used_at=datetime(
            2026,
            8,
            17,
            10,
            30,
        ),
        observations="Cambio preventivo.",
    )

    return WorkOrderSparePartItem(
        usage=usage,
        spare_part=spare_part,
    )


def test_should_present_spare_part_usage():

    result = ListWorkOrderSparePartsResult(
        items=[
            create_item()
        ]
    )

    view_model = (
        WorkOrderSparePartsPresenter.present(
            result
        )
    )

    assert view_model.has_items is True
    assert view_model.total_items == 1
    assert view_model.total_cost == 31.0

    item = view_model.items[0]

    assert item.code == "SP-001"
    assert item.name == "Rodamiento"
    assert item.manufacturer == "SKF"
    assert item.part_number == "6204"
    assert item.unit == "pieza"
    assert item.quantity == 2
    assert item.unit_cost == 15.5
    assert item.total_cost == 31.0

    assert (
        item.used_at
        == "17/08/2026 10:30"
    )

    assert (
        item.observations
        == "Cambio preventivo."
    )


def test_should_use_default_catalog_values():

    result = ListWorkOrderSparePartsResult(
        items=[
            create_item(
                manufacturer="",
                part_number="",
            )
        ]
    )

    view_model = (
        WorkOrderSparePartsPresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert (
        item.manufacturer
        == "Sin fabricante"
    )

    assert (
        item.part_number
        == "Sin número de parte"
    )


def test_should_calculate_total_cost():

    first = create_item()
    second = create_item()

    result = ListWorkOrderSparePartsResult(
        items=[
            first,
            second,
        ]
    )

    view_model = (
        WorkOrderSparePartsPresenter.present(
            result
        )
    )

    assert view_model.total_items == 2
    assert view_model.total_cost == 62.0


def test_should_present_empty_result():

    result = ListWorkOrderSparePartsResult(
        items=[]
    )

    view_model = (
        WorkOrderSparePartsPresenter.present(
            result
        )
    )

    assert view_model.has_items is False
    assert view_model.total_items == 0
    assert view_model.total_cost == 0
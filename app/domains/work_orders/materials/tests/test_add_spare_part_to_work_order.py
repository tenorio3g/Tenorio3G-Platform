from datetime import datetime

import pytest

from app.domains.assets.spare_parts.entities import (
    SparePart,
)

from app.domains.assets.spare_parts.repositories import (
    InMemorySparePartRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.materials.repositories import (
    InMemoryWorkOrderSparePartUsageRepository,
)

from app.domains.work_orders.materials.use_cases import (
    AddSparePartToWorkOrder,
    AddSparePartToWorkOrderCommand,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Orden de prueba",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=datetime(
            2026,
            8,
            17,
            16,
            0,
        ),
    )


def build_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    spare_part_repository = (
        InMemorySparePartRepository()
    )

    usage_repository = (
        InMemoryWorkOrderSparePartUsageRepository()
    )

    use_case = AddSparePartToWorkOrder(
        work_order_repository,
        spare_part_repository,
        usage_repository,
    )

    return (
        work_order_repository,
        spare_part_repository,
        usage_repository,
        use_case,
    )


def create_command():

    return AddSparePartToWorkOrderCommand(
        work_order_code="WO-001",
        spare_part_code="SP-001",
        quantity=2,
        unit_cost=15.5,
        used_at=datetime(
            2026,
            8,
            17,
            17,
            0,
        ),
        observations="Cambio preventivo.",
    )


def test_should_add_spare_part_to_work_order():

    (
        work_order_repository,
        spare_part_repository,
        usage_repository,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    spare_part_repository.save_spare_part(
        SparePart(
            code="SP-001",
            name="Rodamiento",
            manufacturer="SKF",
            part_number="6204",
            unit="pieza",
        )
    )

    result = use_case.execute(
        create_command()
    )

    assert (
        result.usage.work_order_code
        == "WO-001"
    )

    assert (
        result.usage.spare_part_code
        == "SP-001"
    )

    assert result.usage.quantity == 2
    assert result.usage.total_cost == 31.0

    persisted = (
        usage_repository
        .list_by_work_order(
            "WO-001"
        )
    )

    assert len(persisted) == 1


def test_should_reject_unknown_work_order():

    (
        _,
        spare_part_repository,
        _,
        use_case,
    ) = build_use_case()

    spare_part_repository.save_spare_part(
        SparePart(
            code="SP-001",
            name="Rodamiento",
        )
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_spare_part():

    (
        work_order_repository,
        _,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    with pytest.raises(
        ValueError,
        match="spare part not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_normalize_work_order_code():

    (
        work_order_repository,
        spare_part_repository,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    spare_part_repository.save_spare_part(
        SparePart(
            code="SP-001",
            name="Rodamiento",
        )
    )

    command = AddSparePartToWorkOrderCommand(
        work_order_code=" wo-001 ",
        spare_part_code=" SP-001 ",
        quantity=1,
        used_at=datetime(
            2026,
            8,
            17,
        ),
    )

    result = use_case.execute(
        command
    )

    assert (
        result.usage.work_order_code
        == "WO-001"
    )

    assert (
        result.usage.spare_part_code
        == "SP-001"
    )
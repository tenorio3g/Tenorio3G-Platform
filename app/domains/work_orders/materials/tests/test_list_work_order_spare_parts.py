from datetime import datetime

from app.domains.assets.spare_parts.entities import (
    SparePart,
)

from app.domains.assets.spare_parts.repositories import (
    InMemorySparePartRepository,
)

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.repositories import (
    InMemoryWorkOrderSparePartUsageRepository,
)

from app.domains.work_orders.materials.use_cases import (
    ListWorkOrderSpareParts,
    ListWorkOrderSparePartsQuery,
)


def build_use_case():

    usage_repository = (
        InMemoryWorkOrderSparePartUsageRepository()
    )

    spare_part_repository = (
        InMemorySparePartRepository()
    )

    use_case = ListWorkOrderSpareParts(
        usage_repository,
        spare_part_repository,
    )

    return (
        usage_repository,
        spare_part_repository,
        use_case,
    )


def test_should_list_work_order_spare_parts():

    (
        usage_repository,
        spare_part_repository,
        use_case,
    ) = build_use_case()

    spare_part_repository.save_spare_part(
        SparePart(
            code="SP-001",
            name="Rodamiento",
            manufacturer="SKF",
            part_number="6204",
            unit="pieza",
        )
    )

    usage_repository.save(
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
            quantity=2,
            unit_cost=15.5,
            used_at=datetime(
                2026,
                8,
                17,
                10,
                0,
            ),
        )
    )

    result = use_case.execute(
        ListWorkOrderSparePartsQuery(
            work_order_code="WO-001"
        )
    )

    assert len(result.items) == 1

    item = result.items[0]

    assert item.spare_part.code == "SP-001"
    assert item.spare_part.name == "Rodamiento"
    assert item.spare_part.manufacturer == "SKF"

    assert item.usage.quantity == 2
    assert item.usage.total_cost == 31.0


def test_should_return_empty_result():

    (
        _,
        _,
        use_case,
    ) = build_use_case()

    result = use_case.execute(
        ListWorkOrderSparePartsQuery(
            work_order_code="WO-001"
        )
    )

    assert result.items == []


def test_should_normalize_work_order_code():

    (
        usage_repository,
        spare_part_repository,
        use_case,
    ) = build_use_case()

    spare_part_repository.save_spare_part(
        SparePart(
            code="SP-001",
            name="Rodamiento",
        )
    )

    usage_repository.save(
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-001",
            quantity=1,
            used_at=datetime(
                2026,
                8,
                17,
            ),
        )
    )

    result = use_case.execute(
        ListWorkOrderSparePartsQuery(
            work_order_code=" wo-001 "
        )
    )

    assert len(result.items) == 1


def test_should_ignore_missing_catalog_spare_part():

    (
        usage_repository,
        _,
        use_case,
    ) = build_use_case()

    usage_repository.save(
        WorkOrderSparePartUsage(
            work_order_code="WO-001",
            spare_part_code="SP-MISSING",
            quantity=1,
            used_at=datetime(
                2026,
                8,
                17,
            ),
        )
    )

    result = use_case.execute(
        ListWorkOrderSparePartsQuery(
            work_order_code="WO-001"
        )
    )

    assert result.items == []
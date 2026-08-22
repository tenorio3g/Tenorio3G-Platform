from datetime import datetime

from app.domains.assets.entities import (
    Asset,
)

from app.domains.assets.repositories.in_memory_asset_repository import (
    InMemoryAssetRepository,
)

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.repositories import (
    InMemoryWorkOrderTechnicianAssignmentRepository,
)

from app.domains.work_orders.use_cases.list_work_order_summaries import (
    ListWorkOrderSummaries,
)


def create_work_order(
    code="WO-001",
    created_at=None,
):

    return WorkOrder(
        code=code,
        title="Inspección general",
        description="Prueba.",
        work_type="PREVENTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="REQ-001",
        supervisor_person_code="SUP-001",
        created_at=(
            created_at
            or datetime(
                2026,
                8,
                21,
                8,
                0,
            )
        ),
    )


def build_use_case():

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    asset_repository = (
        InMemoryAssetRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    technician_repository = (
        InMemoryWorkOrderTechnicianAssignmentRepository()
    )

    use_case = ListWorkOrderSummaries(
        work_order_repository,
        asset_repository,
        person_repository,
        technician_repository,
    )

    return (
        work_order_repository,
        asset_repository,
        person_repository,
        technician_repository,
        use_case,
    )


def configure_common_data(
    asset_repository,
    person_repository,
):

    asset_repository.save(
        Asset(
            code="ASSET-001",
            name="TABLERO GENERAL",
            asset_model_code="MODEL-001",
            serial_number="SN-001",
            installation_date=datetime(
                2025,
                1,
                15,
            ),
            status="OPERATING",
            location_code="MD1",
        )
    )

    person_repository.save(
        Person(
            code="REQ-001",
            name="Solicitante",
        )
    )

    person_repository.save(
        Person(
            code="SUP-001",
            name="Supervisor",
        )
    )

    person_repository.save(
        Person(
            code="TEC-001",
            name="Angel",
        )
    )

    person_repository.save(
        Person(
            code="TEC-002",
            name="Nato",
        )
    )


def test_should_list_work_order_summary():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        technician_repository,
        use_case,
    ) = build_use_case()

    configure_common_data(
        asset_repository,
        person_repository,
    )

    work_order_repository.save(
        create_work_order()
    )

    technician_repository.save(
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="TEC-001",
            assigned_at=datetime(
                2026,
                8,
                21,
                9,
                0,
            ),
        )
    )

    result = use_case.execute()

    assert len(result.items) == 1

    item = result.items[0]

    assert item.work_order.code == "WO-001"
    assert item.asset.name == "TABLERO GENERAL"
    assert item.requester.name == "Solicitante"
    assert item.supervisor.name == "Supervisor"

    assert [
        person.code
        for person in item.active_technicians
    ] == [
        "TEC-001"
    ]


def test_should_distinguish_active_and_historical_technicians():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        technician_repository,
        use_case,
    ) = build_use_case()

    configure_common_data(
        asset_repository,
        person_repository,
    )

    work_order_repository.save(
        create_work_order()
    )

    active_assignment = (
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="TEC-001",
            assigned_at=datetime(
                2026,
                8,
                21,
                9,
                0,
            ),
        )
    )

    historical_assignment = (
        WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code="TEC-002",
            assigned_at=datetime(
                2026,
                8,
                21,
                10,
                0,
            ),
        )
    )

    historical_assignment.unassign(
        datetime(
            2026,
            8,
            21,
            12,
            0,
        )
    )

    technician_repository.save(
        active_assignment
    )

    technician_repository.save(
        historical_assignment
    )

    result = use_case.execute()

    item = result.items[0]

    assert {
        person.code
        for person in item.active_technicians
    } == {
        "TEC-001"
    }

    assert {
        person.code
        for person in item.participant_technicians
    } == {
        "TEC-001",
        "TEC-002",
    }


def test_should_order_newest_work_orders_first():

    (
        work_order_repository,
        asset_repository,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    configure_common_data(
        asset_repository,
        person_repository,
    )

    work_order_repository.save(
        create_work_order(
            code="WO-001",
            created_at=datetime(
                2026,
                8,
                20,
                8,
                0,
            ),
        )
    )

    work_order_repository.save(
        create_work_order(
            code="WO-002",
            created_at=datetime(
                2026,
                8,
                21,
                8,
                0,
            ),
        )
    )

    result = use_case.execute()

    assert [
        item.work_order.code
        for item in result.items
    ] == [
        "WO-002",
        "WO-001",
    ]


def test_should_tolerate_missing_related_data():

    (
        work_order_repository,
        _,
        _,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.save(
        create_work_order()
    )

    result = use_case.execute()

    item = result.items[0]

    assert item.asset is None
    assert item.requester is None
    assert item.supervisor is None
    assert item.active_technicians == []
    assert item.participant_technicians == []
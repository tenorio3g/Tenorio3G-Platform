from datetime import datetime

import pytest

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def create_work_order():

    return WorkOrder(
        code="wo-001",
        title=" Inspección de tablero ",
        description=" Revisión general. ",
        work_type=" preventive ",
        priority=" high ",
        asset_code=" asset-001 ",
        requester_person_code=" req-001 ",
        supervisor_person_code=" sup-001 ",
        created_at=datetime(
            2026,
            8,
            15,
            8,
            0,
        ),
    )


def test_should_create_work_order():

    work_order = create_work_order()

    assert work_order.code == "WO-001"

    assert (
        work_order.title
        == "Inspección de tablero"
    )

    assert (
        work_order.description
        == "Revisión general."
    )

    assert (
        work_order.work_type
        == "PREVENTIVE"
    )

    assert work_order.priority == "HIGH"

    assert (
        work_order.asset_code
        == "ASSET-001"
    )

    assert (
        work_order.requester_person_code
        == "REQ-001"
    )

    assert (
        work_order.supervisor_person_code
        == "SUP-001"
    )

    assert (
        work_order.status
        == WorkOrderStatus.CREATED
    )


@pytest.mark.parametrize(
    "field_name",
    [
        "code",
        "title",
        "work_type",
        "priority",
    ],
)
def test_should_require_mandatory_fields(
    field_name,
):

    data = {
        "code": "WO-001",
        "title": "Inspección",
        "description": "",
        "work_type": "PREVENTIVE",
        "priority": "HIGH",
        "asset_code": "ASSET-001",
        "requester_person_code": "REQ-001",
        "supervisor_person_code": "SUP-001",
        "created_at": datetime(
            2026,
            8,
            15,
        ),
    }

    data[field_name] = ""

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        WorkOrder(
            **data
        )


def test_should_require_created_at_datetime():

    with pytest.raises(
        ValueError,
        match="created_at must be a datetime",
    ):
        WorkOrder(
            code="WO-001",
            title="Inspección",
            description="",
            work_type="PREVENTIVE",
            priority="HIGH",
            asset_code="ASSET-001",
            requester_person_code="REQ-001",
            supervisor_person_code="SUP-001",
            created_at="2026-08-15",
        )


def test_should_require_valid_status():

    with pytest.raises(
        ValueError,
        match="status must be a WorkOrderStatus",
    ):
        WorkOrder(
            code="WO-001",
            title="Inspección",
            description="",
            work_type="PREVENTIVE",
            priority="HIGH",
            asset_code="ASSET-001",
            requester_person_code="REQ-001",
            supervisor_person_code="SUP-001",
            created_at=datetime(
                2026,
                8,
                15,
            ),
            status="CREATED",
        )

def test_should_follow_main_work_order_lifecycle():

    work_order = create_work_order()

    work_order.assign()
    assert work_order.status == WorkOrderStatus.ASSIGNED

    work_order.start()
    assert work_order.status == WorkOrderStatus.IN_PROGRESS

    work_order.hold()
    assert work_order.status == WorkOrderStatus.ON_HOLD

    work_order.resume()
    assert work_order.status == WorkOrderStatus.IN_PROGRESS

    work_order.complete()
    assert work_order.status == WorkOrderStatus.COMPLETED

    work_order.close()
    assert work_order.status == WorkOrderStatus.CLOSED


def test_should_not_start_created_work_order():

    work_order = create_work_order()

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot be started from current status"
        ),
    ):
        work_order.start()


def test_should_not_complete_assigned_work_order():

    work_order = create_work_order()

    work_order.assign()

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot be completed from current status"
        ),
    ):
        work_order.complete()


def test_should_cancel_created_work_order():

    work_order = create_work_order()

    work_order.cancel()

    assert (
        work_order.status
        == WorkOrderStatus.CANCELLED
    )


def test_should_not_cancel_completed_work_order():

    work_order = create_work_order()

    work_order.assign()
    work_order.start()
    work_order.complete()

    with pytest.raises(
        ValueError,
        match=(
            "work order cannot be cancelled from current status"
        ),
    ):
        work_order.cancel()
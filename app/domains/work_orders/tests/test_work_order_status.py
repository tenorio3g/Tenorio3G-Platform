from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


def test_should_define_created_status():

    assert (
        WorkOrderStatus.CREATED.value
        == "CREATED"
    )


def test_should_define_assigned_status():

    assert (
        WorkOrderStatus.ASSIGNED.value
        == "ASSIGNED"
    )


def test_should_define_in_progress_status():

    assert (
        WorkOrderStatus.IN_PROGRESS.value
        == "IN_PROGRESS"
    )


def test_should_define_on_hold_status():

    assert (
        WorkOrderStatus.ON_HOLD.value
        == "ON_HOLD"
    )


def test_should_define_completed_status():

    assert (
        WorkOrderStatus.COMPLETED.value
        == "COMPLETED"
    )


def test_should_define_closed_status():

    assert (
        WorkOrderStatus.CLOSED.value
        == "CLOSED"
    )


def test_should_define_cancelled_status():

    assert (
        WorkOrderStatus.CANCELLED.value
        == "CANCELLED"
    )
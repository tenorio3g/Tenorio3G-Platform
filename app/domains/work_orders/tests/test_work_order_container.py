
import pytest
from app.domains.work_orders.bootstrap import (
    assign_work_order,
    cancel_work_order,
    close_work_order,
    complete_work_order,
    create_work_order,
    get_work_order,
    hold_work_order,
    list_work_orders,
    list_work_orders_by_asset,
    resume_work_order,
    start_work_order,
    work_order_repository,
    get_work_order_detail,
)

from app.domains.work_orders.repositories import (
    SQLiteWorkOrderRepository,
)


from app.domains.work_orders.use_cases import (
    AssignWorkOrder,
    CancelWorkOrder,
    CloseWorkOrder,
    CompleteWorkOrder,
    CreateWorkOrder,
    GetWorkOrder,
    HoldWorkOrder,
    ListWorkOrders,
    ListWorkOrdersByAsset,
    ResumeWorkOrder,
    StartWorkOrder,
    GetWorkOrderDetail
)

def test_work_order_container_should_build_repository():

    assert isinstance(
        work_order_repository,
        SQLiteWorkOrderRepository,
    )


def test_work_order_container_should_build_create_use_case():

    assert isinstance(
        create_work_order,
        CreateWorkOrder,
    )


def test_work_order_container_should_build_get_use_case():

    assert isinstance(
        get_work_order,
        GetWorkOrder,
    )


def test_work_order_container_should_build_list_use_case():

    assert isinstance(
        list_work_orders,
        ListWorkOrders,
    )


def test_work_order_container_should_build_list_by_asset_use_case():

    assert isinstance(
        list_work_orders_by_asset,
        ListWorkOrdersByAsset,
    )

@pytest.mark.parametrize(
    "instance, expected_type",
    [
        (
            assign_work_order,
            AssignWorkOrder,
        ),
        (
            start_work_order,
            StartWorkOrder,
        ),
        (
            hold_work_order,
            HoldWorkOrder,
        ),
        (
            resume_work_order,
            ResumeWorkOrder,
        ),
        (
            complete_work_order,
            CompleteWorkOrder,
        ),
        (
            close_work_order,
            CloseWorkOrder,
        ),
        (
            cancel_work_order,
            CancelWorkOrder,
        ),
    ],
)
def test_work_order_container_should_build_lifecycle_use_cases(
    instance,
    expected_type,
):

    assert isinstance(
        instance,
        expected_type,
    )

def test_work_order_container_should_build_detail_use_case():

    assert isinstance(
        get_work_order_detail,
        GetWorkOrderDetail,
    )
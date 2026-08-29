from datetime import datetime
from types import SimpleNamespace

from app.core.dashboard import (
    DashboardService,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


class FakeAssetRepository:

    def find_all(self):
        return []


class FakeWorkOrderRepository:

    def list_all(self):
        return [
            SimpleNamespace(
                code="WO-001",
                title="Orden autorizada",
                status=WorkOrderStatus.APPROVED,
                priority="MEDIUM",
                asset_code="ASSET-001",
                created_at=datetime(
                    2026,
                    8,
                    29,
                    9,
                    0,
                ),
            ),
        ]


class FakePersonRepository:

    def list_all(self):
        return []


class FakeActivityRepository:

    def list_by_work_order(
        self,
        work_order_code,
    ):
        return []


def test_should_count_approved_work_orders():

    service = DashboardService(
        asset_repository=(
            FakeAssetRepository()
        ),
        work_order_repository=(
            FakeWorkOrderRepository()
        ),
        person_repository=(
            FakePersonRepository()
        ),
        activity_repository=(
            FakeActivityRepository()
        ),
    )

    dashboard = service.build()

    assert dashboard.total_work_orders == 1
    assert dashboard.approved_work_orders == 1

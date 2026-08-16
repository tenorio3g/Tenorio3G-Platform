from app.domains.work_orders.entities import (
    WorkOrder,
)

from .work_order_repository import (
    WorkOrderRepository,
)


class InMemoryWorkOrderRepository(
    WorkOrderRepository,
):

    def __init__(
        self,
    ):
        self._work_orders: dict[
            str,
            WorkOrder,
        ] = {}

    def save(
        self,
        work_order: WorkOrder,
    ) -> None:

        self._work_orders[
            work_order.code
        ] = work_order

    def get_by_code(
        self,
        code: str,
    ) -> WorkOrder | None:

        normalized_code = str(
            code
        ).strip().upper()

        return self._work_orders.get(
            normalized_code
        )

    def list_all(
        self,
    ) -> list[WorkOrder]:

        return list(
            self._work_orders.values()
        )

    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[WorkOrder]:

        normalized_asset_code = str(
            asset_code
        ).strip().upper()

        return [
            work_order
            for work_order
            in self._work_orders.values()
            if work_order.asset_code
            == normalized_asset_code
        ]

    def delete(
        self,
        code: str,
    ) -> None:

        normalized_code = str(
            code
        ).strip().upper()

        self._work_orders.pop(
            normalized_code,
            None,
        )
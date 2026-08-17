from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from .work_order_activity_repository import (
    WorkOrderActivityRepository,
)


class InMemoryWorkOrderActivityRepository(
    WorkOrderActivityRepository,
):

    def __init__(
        self,
    ):
        self._activities: dict[
            str,
            WorkOrderActivity,
        ] = {}

    def save(
        self,
        activity: WorkOrderActivity,
    ) -> None:

        self._activities[
            activity.code
        ] = activity

    def get_by_code(
        self,
        code: str,
    ) -> WorkOrderActivity | None:

        normalized_code = str(
            code
        ).strip().upper()

        return self._activities.get(
            normalized_code
        )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderActivity]:

        normalized_work_order_code = str(
            work_order_code
        ).strip().upper()

        return [
            activity
            for activity
            in self._activities.values()
            if activity.work_order_code
            == normalized_work_order_code
        ]

    def delete(
        self,
        code: str,
    ) -> None:

        normalized_code = str(
            code
        ).strip().upper()

        self._activities.pop(
            normalized_code,
            None,
        )
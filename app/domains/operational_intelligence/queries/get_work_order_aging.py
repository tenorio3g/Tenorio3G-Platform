from dataclasses import dataclass
from datetime import (
    datetime,
    timedelta,
)

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.foundation.timeline.engine.use_cases import (
    ListTimelineEventsQuery,
)


@dataclass(frozen=True)
class WorkOrderAgingItem:
    work_order_code: str
    status: WorkOrderStatus
    created_at: datetime
    status_since: datetime | None
    age: timedelta
    time_in_current_status: timedelta | None


class GetWorkOrderAging:

    OPEN_STATUSES = {
        WorkOrderStatus.CREATED,
        WorkOrderStatus.APPROVED,
        WorkOrderStatus.ASSIGNED,
        WorkOrderStatus.IN_PROGRESS,
        WorkOrderStatus.ON_HOLD,
    }

    STATUS_EVENTS = {
        WorkOrderStatus.APPROVED: {
            "WORK_ORDER_APPROVED",
        },
        WorkOrderStatus.ASSIGNED: {
            "WORK_ORDER_ASSIGNED",
        },
        WorkOrderStatus.IN_PROGRESS: {
            "WORK_ORDER_STARTED",
            "WORK_ORDER_RESUMED",
        },
        WorkOrderStatus.ON_HOLD: {
            "WORK_ORDER_HELD",
        },
    }

    def __init__(
        self,
        work_order_repository,
        list_timeline_events,
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._list_timeline_events = (
            list_timeline_events
        )

    def execute(
        self,
        now: datetime,
    ) -> list[WorkOrderAgingItem]:

        if not isinstance(
            now,
            datetime,
        ):
            raise ValueError(
                "now must be a datetime"
            )

        result = []

        work_orders = (
            self._work_order_repository
            .list_all()
        )

        for work_order in work_orders:

            if (
                work_order.status
                not in self.OPEN_STATUSES
            ):
                continue

            status_since = (
                self._resolve_status_since(
                    work_order=work_order,
                )
            )

            time_in_current_status = None

            if status_since is not None:
                time_in_current_status = (
                    now
                    - status_since
                )

            result.append(
                WorkOrderAgingItem(
                    work_order_code=(
                        work_order.code
                    ),
                    status=(
                        work_order.status
                    ),
                    created_at=(
                        work_order.created_at
                    ),
                    status_since=(
                        status_since
                    ),
                    age=(
                        now
                        - work_order.created_at
                    ),
                    time_in_current_status=(
                        time_in_current_status
                    ),
                )
            )

        return result

    def _resolve_status_since(
        self,
        work_order,
    ) -> datetime | None:

        if (
            work_order.status
            == WorkOrderStatus.CREATED
        ):
            return work_order.created_at

        expected_events = (
            self.STATUS_EVENTS.get(
                work_order.status
            )
        )

        if not expected_events:
            return None

        timeline = (
            self._list_timeline_events
            .execute(
                ListTimelineEventsQuery(
                    entity_type="WORK_ORDER",
                    entity_code=(
                        work_order.code
                    ),
                )
            )
        )

        for event in timeline.items:
            if (
                event.event_type
                in expected_events
            ):
                return event.occurred_at

        return None

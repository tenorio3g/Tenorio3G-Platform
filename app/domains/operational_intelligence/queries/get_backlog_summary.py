from dataclasses import dataclass
from datetime import timedelta

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from .get_work_order_aging import (
    WorkOrderAgingItem,
)


@dataclass(frozen=True)
class BacklogSummary:
    total_open: int

    created: int
    approved: int
    assigned: int
    in_progress: int
    on_hold: int

    average_age: timedelta | None
    oldest_age: timedelta | None


class GetBacklogSummary:

    OPEN_STATUSES = {
        WorkOrderStatus.CREATED,
        WorkOrderStatus.APPROVED,
        WorkOrderStatus.ASSIGNED,
        WorkOrderStatus.IN_PROGRESS,
        WorkOrderStatus.ON_HOLD,
    }

    def execute(
        self,
        items: list[WorkOrderAgingItem],
    ) -> BacklogSummary:

        valid_items = [
            item
            for item in items
            if item.status in self.OPEN_STATUSES
        ]

        counters = {
            status: 0
            for status in self.OPEN_STATUSES
        }

        for item in valid_items:
            counters[
                item.status
            ] += 1

        total_open = len(
            valid_items
        )

        if total_open == 0:
            average_age = None
            oldest_age = None
        else:
            total_age = sum(
                (
                    item.age
                    for item in valid_items
                ),
                timedelta(),
            )

            average_age = (
                total_age
                / total_open
            )

            oldest_age = max(
                item.age
                for item in valid_items
            )

        return BacklogSummary(
            total_open=total_open,
            created=counters[
                WorkOrderStatus.CREATED
            ],
            approved=counters[
                WorkOrderStatus.APPROVED
            ],
            assigned=counters[
                WorkOrderStatus.ASSIGNED
            ],
            in_progress=counters[
                WorkOrderStatus.IN_PROGRESS
            ],
            on_hold=counters[
                WorkOrderStatus.ON_HOLD
            ],
            average_age=average_age,
            oldest_age=oldest_age,
        )

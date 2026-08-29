from dataclasses import dataclass

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


@dataclass(frozen=True)
class WorkOrderStatusSummary:
    created: int
    approved: int
    assigned: int
    in_progress: int
    on_hold: int
    completed: int
    closed: int
    cancelled: int

    @property
    def open_total(self) -> int:
        return (
            self.created
            + self.approved
            + self.assigned
            + self.in_progress
            + self.on_hold
        )

    @property
    def terminal_total(self) -> int:
        return (
            self.completed
            + self.closed
            + self.cancelled
        )

    @property
    def total(self) -> int:
        return (
            self.open_total
            + self.terminal_total
        )


class GetWorkOrderStatusSummary:

    def __init__(
        self,
        work_order_repository,
    ):
        self._work_order_repository = (
            work_order_repository
        )

    def execute(
        self,
    ) -> WorkOrderStatusSummary:

        work_orders = (
            self._work_order_repository
            .list_all()
        )

        counters = {
            status: 0
            for status
            in WorkOrderStatus
        }

        for work_order in work_orders:
            counters[
                work_order.status
            ] += 1

        return WorkOrderStatusSummary(
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
            completed=counters[
                WorkOrderStatus.COMPLETED
            ],
            closed=counters[
                WorkOrderStatus.CLOSED
            ],
            cancelled=counters[
                WorkOrderStatus.CANCELLED
            ],
        )

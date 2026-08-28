from dataclasses import dataclass
from datetime import datetime

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.timeline import (
    WorkOrderTimelineRecorder,
)


@dataclass(frozen=True)
class CompleteWorkOrderCommand:
    code: str
    actor_person_code: str
    occurred_at: datetime


@dataclass(frozen=True)
class CompleteWorkOrderResult:
    work_order: WorkOrder


class CompleteWorkOrder:

    def __init__(
        self,
        repository: WorkOrderRepository,
        timeline_recorder: WorkOrderTimelineRecorder | None = None,
    ):
        self._repository = repository

        self._timeline_recorder = (
            timeline_recorder
        )

    def execute(
        self,
        command: CompleteWorkOrderCommand,
    ) -> CompleteWorkOrderResult:

        work_order = self._repository.get_by_code(
            command.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        work_order.complete()

        self._repository.save(
            work_order
        )

        if self._timeline_recorder is not None:

            self._timeline_recorder.record(
                work_order_code=work_order.code,
                event_type="WORK_ORDER_COMPLETED",
                actor_person_code=(
                    command.actor_person_code
                ),
                occurred_at=(
                    command.occurred_at
                ),
            )

        return CompleteWorkOrderResult(
            work_order=work_order
        )
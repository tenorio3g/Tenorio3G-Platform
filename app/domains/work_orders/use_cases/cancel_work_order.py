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
class CancelWorkOrderCommand:
    code: str
    actor_person_code: str
    occurred_at: datetime


@dataclass(frozen=True)
class CancelWorkOrderResult:
    work_order: WorkOrder


class CancelWorkOrder:

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
        command: CancelWorkOrderCommand,
    ) -> CancelWorkOrderResult:

        work_order = self._repository.get_by_code(
            command.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        work_order.cancel()

        self._repository.save(
            work_order
        )

        if self._timeline_recorder is not None:

            self._timeline_recorder.record(
                work_order_code=work_order.code,
                event_type="WORK_ORDER_CANCELLED",
                actor_person_code=(
                    command.actor_person_code
                ),
                occurred_at=(
                    command.occurred_at
                ),
            )

        return CancelWorkOrderResult(
            work_order=work_order
        )
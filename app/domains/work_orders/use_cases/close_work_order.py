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
class CloseWorkOrderCommand:
    code: str
    actor_person_code: str
    occurred_at: datetime


@dataclass(frozen=True)
class CloseWorkOrderResult:
    work_order: WorkOrder


class CloseWorkOrder:

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
        command: CloseWorkOrderCommand,
    ) -> CloseWorkOrderResult:

        work_order = self._repository.get_by_code(
            command.code
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        work_order.close()

        self._repository.save(
            work_order
        )

        if self._timeline_recorder is not None:

            self._timeline_recorder.record(
                work_order_code=work_order.code,
                event_type="WORK_ORDER_CLOSED",
                actor_person_code=(
                    command.actor_person_code
                ),
                occurred_at=(
                    command.occurred_at
                ),
            )

        return CloseWorkOrderResult(
            work_order=work_order
        )
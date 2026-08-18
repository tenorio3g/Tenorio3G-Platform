from dataclasses import dataclass
from datetime import datetime

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.repositories import (
    WorkOrderToolUsageRepository,
)


@dataclass(frozen=True)
class IssueToolToWorkOrderCommand:
    usage_id: str
    work_order_code: str
    tool_code: str
    tool_name: str
    quantity: int
    issued_at: datetime
    observations: str = ""


@dataclass(frozen=True)
class IssueToolToWorkOrderResult:
    usage: WorkOrderToolUsage


class IssueToolToWorkOrder:

    def __init__(
        self,
        repository: WorkOrderToolUsageRepository,
        work_order_repository: WorkOrderRepository,
    ):
        self._repository = repository
        self._work_order_repository = (
            work_order_repository
        )

    def execute(
        self,
        command: IssueToolToWorkOrderCommand,
    ) -> IssueToolToWorkOrderResult:

        work_order = (
            self._work_order_repository
            .get_by_code(
                command.work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        usage = WorkOrderToolUsage(
            usage_id=command.usage_id,
            work_order_code=work_order.code,
            tool_code=command.tool_code,
            tool_name=command.tool_name,
            quantity=command.quantity,
            issued_at=command.issued_at,
            observations=command.observations,
        )

        self._repository.save(
            usage
        )

        return IssueToolToWorkOrderResult(
            usage=usage
        )
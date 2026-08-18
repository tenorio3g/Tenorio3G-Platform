from dataclasses import dataclass
from datetime import datetime

from app.domains.work_orders.tools.entities import (
    WorkOrderToolUsage,
)

from app.domains.work_orders.tools.repositories import (
    WorkOrderToolUsageRepository,
)


@dataclass(frozen=True)
class ReturnToolFromWorkOrderCommand:
    usage_id: str
    returned_at: datetime


@dataclass(frozen=True)
class ReturnToolFromWorkOrderResult:
    usage: WorkOrderToolUsage


class ReturnToolFromWorkOrder:

    def __init__(
        self,
        repository: WorkOrderToolUsageRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: ReturnToolFromWorkOrderCommand,
    ) -> ReturnToolFromWorkOrderResult:

        usage = self._repository.get_by_id(
            command.usage_id
        )

        if usage is None:
            raise ValueError(
                "tool usage not found"
            )

        usage.return_tool(
            command.returned_at
        )

        self._repository.save(
            usage
        )

        return ReturnToolFromWorkOrderResult(
            usage=usage
        )
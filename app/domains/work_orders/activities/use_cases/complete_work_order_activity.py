from dataclasses import dataclass
from datetime import datetime

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)


@dataclass(frozen=True)
class CompleteWorkOrderActivityCommand:
    code: str
    completed_at: datetime


@dataclass(frozen=True)
class CompleteWorkOrderActivityResult:
    activity: WorkOrderActivity


class CompleteWorkOrderActivity:

    def __init__(
        self,
        repository: WorkOrderActivityRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: CompleteWorkOrderActivityCommand,
    ) -> CompleteWorkOrderActivityResult:

        activity = self._repository.get_by_code(
            command.code
        )

        if activity is None:
            raise ValueError(
                "activity not found"
            )

        activity.complete(
            command.completed_at
        )

        self._repository.save(
            activity
        )

        return CompleteWorkOrderActivityResult(
            activity=activity
        )
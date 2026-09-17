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
    completion_notes: str = ""


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

        completion_notes = str(
            command.completion_notes
        ).strip()

        if not completion_notes:
            raise ValueError(
                "completion_notes is required"
            )

        activity.complete(
            command.completed_at,
            completion_notes=completion_notes,
        )

        self._repository.save(
            activity
        )

        return CompleteWorkOrderActivityResult(
            activity=activity
        )
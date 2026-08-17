from dataclasses import dataclass
from datetime import datetime

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)


@dataclass(frozen=True)
class StartWorkOrderActivityCommand:
    code: str
    started_at: datetime


@dataclass(frozen=True)
class StartWorkOrderActivityResult:
    activity: WorkOrderActivity


class StartWorkOrderActivity:

    def __init__(
        self,
        repository: WorkOrderActivityRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: StartWorkOrderActivityCommand,
    ) -> StartWorkOrderActivityResult:

        activity = self._repository.get_by_code(
            command.code
        )

        if activity is None:
            raise ValueError(
                "activity not found"
            )

        activity.start(
            command.started_at
        )

        self._repository.save(
            activity
        )

        return StartWorkOrderActivityResult(
            activity=activity
        )
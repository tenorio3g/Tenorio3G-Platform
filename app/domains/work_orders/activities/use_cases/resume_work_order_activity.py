from dataclasses import dataclass
from datetime import datetime

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from app.domains.work_orders.activities.holds.repositories import (
    ActivityHoldRepository,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)


@dataclass(frozen=True)
class ResumeWorkOrderActivityCommand:
    code: str
    resumed_at: datetime
    resumed_by_person_code: str


@dataclass(frozen=True)
class ResumeWorkOrderActivityResult:
    activity: WorkOrderActivity
    hold: ActivityHold


class ResumeWorkOrderActivity:

    def __init__(
        self,
        activity_repository: WorkOrderActivityRepository,
        hold_repository: ActivityHoldRepository,
    ):
        self._activity_repository = (
            activity_repository
        )

        self._hold_repository = (
            hold_repository
        )


    def execute(
        self,
        command: ResumeWorkOrderActivityCommand,
    ) -> ResumeWorkOrderActivityResult:

        activity = (
            self._activity_repository
            .get_by_code(
                command.code
            )
        )

        if activity is None:
            raise ValueError(
                "activity not found"
            )

        active_hold = (
            self._hold_repository
            .get_active_by_activity(
                activity.code
            )
        )

        if active_hold is None:
            raise ValueError(
                "active activity hold not found"
            )

        active_hold.resume(
            resumed_at=command.resumed_at,
            resumed_by_person_code=(
                command.resumed_by_person_code
            ),
        )

        activity.resume()

        self._hold_repository.save(
            active_hold
        )

        self._activity_repository.save(
            activity
        )

        return ResumeWorkOrderActivityResult(
            activity=activity,
            hold=active_hold,
        )

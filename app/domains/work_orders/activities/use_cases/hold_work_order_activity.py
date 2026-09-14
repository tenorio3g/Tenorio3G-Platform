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

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)


@dataclass(frozen=True)
class HoldWorkOrderActivityCommand:
    code: str
    hold_code: str
    reason: ActivityHoldReason
    observations: str
    held_at: datetime
    held_by_person_code: str


@dataclass(frozen=True)
class HoldWorkOrderActivityResult:
    activity: WorkOrderActivity
    hold: ActivityHold


class HoldWorkOrderActivity:

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
        command: HoldWorkOrderActivityCommand,
    ) -> HoldWorkOrderActivityResult:

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

        existing_active_hold = (
            self._hold_repository
            .get_active_by_activity(
                activity.code
            )
        )

        if existing_active_hold is not None:
            raise ValueError(
                "activity already has active hold"
            )

        hold = ActivityHold(
            code=command.hold_code,
            activity_code=activity.code,
            reason=command.reason,
            observations=command.observations,
            held_at=command.held_at,
            held_by_person_code=(
                command.held_by_person_code
            ),
        )

        activity.hold()

        self._activity_repository.save(
            activity
        )

        self._hold_repository.save(
            hold
        )

        return HoldWorkOrderActivityResult(
            activity=activity,
            hold=hold,
        )

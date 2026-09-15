from dataclasses import dataclass, field

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)

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
class ActivityHoldHistoryItem:
    hold: ActivityHold
    held_by_person: Person | None
    resumed_by_person: Person | None


@dataclass(frozen=True)
class WorkOrderActivityItem:
    activity: WorkOrderActivity
    responsible_person: Person
    active_hold: ActivityHold | None = None
    held_by_person: Person | None = None
    hold_history: list[ActivityHoldHistoryItem] = field(
        default_factory=list
    )


@dataclass(frozen=True)
class ListWorkOrderActivitiesQuery:
    work_order_code: str


@dataclass(frozen=True)
class ListWorkOrderActivitiesResult:
    items: list[WorkOrderActivityItem]


class ListWorkOrderActivities:

    def __init__(
        self,
        activity_repository: WorkOrderActivityRepository,
        person_repository: PersonRepository,
        hold_repository: ActivityHoldRepository,
    ):
        self._activity_repository = (
            activity_repository
        )

        self._person_repository = (
            person_repository
        )

        self._hold_repository = (
            hold_repository
        )

    def execute(
        self,
        query: ListWorkOrderActivitiesQuery,
    ) -> ListWorkOrderActivitiesResult:

        activities = (
            self._activity_repository
            .list_by_work_order(
                query.work_order_code
            )
        )

        items = []

        for activity in activities:

            person = (
                self._person_repository
                .get_by_code(
                    activity.responsible_person_code
                )
            )

            if person is None:
                continue

            active_hold = (
                self._hold_repository
                .get_active_by_activity(
                    activity.code
                )
            )

            held_by_person = None

            if active_hold is not None:
                held_by_person = (
                    self._person_repository
                    .get_by_code(
                        active_hold.held_by_person_code
                    )
                )

            holds = (
                self._hold_repository
                .list_by_activity(
                    activity.code
                )
            )

            hold_history = []

            for hold in holds:

                history_held_by_person = (
                    self._person_repository
                    .get_by_code(
                        hold.held_by_person_code
                    )
                )

                history_resumed_by_person = None

                if hold.resumed_by_person_code is not None:
                    history_resumed_by_person = (
                        self._person_repository
                        .get_by_code(
                            hold.resumed_by_person_code
                        )
                    )

                hold_history.append(
                    ActivityHoldHistoryItem(
                        hold=hold,
                        held_by_person=(
                            history_held_by_person
                        ),
                        resumed_by_person=(
                            history_resumed_by_person
                        ),
                    )
                )

            items.append(
                WorkOrderActivityItem(
                    activity=activity,
                    responsible_person=person,
                    active_hold=active_hold,
                    held_by_person=held_by_person,
                    hold_history=hold_history,
                )
            )

        return ListWorkOrderActivitiesResult(
            items=items
        )

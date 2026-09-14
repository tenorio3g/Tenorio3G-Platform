from dataclasses import dataclass

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
class WorkOrderActivityItem:
    activity: WorkOrderActivity
    responsible_person: Person
    active_hold: ActivityHold | None = None


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

            items.append(
                WorkOrderActivityItem(
                    activity=activity,
                    responsible_person=person,
                    active_hold=active_hold,
                )
            )

        return ListWorkOrderActivitiesResult(
            items=items
        )

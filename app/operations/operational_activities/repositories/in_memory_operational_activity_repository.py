from datetime import date, datetime, time, timedelta

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
)
from app.operations.operational_activities.repositories.operational_activity_repository import (
    OperationalActivityRepository,
)


class InMemoryOperationalActivityRepository(OperationalActivityRepository):

    def __init__(self):
        self._activities: dict[
            str,
            OperationalActivity,
        ] = {}

    def save(
        self,
        activity: OperationalActivity,
    ) -> None:
        self._activities[activity.code] = activity

    def get_by_code(
        self,
        code: str,
    ) -> OperationalActivity | None:
        return self._activities.get(code)

    def list_all(
        self,
    ) -> list[OperationalActivity]:
        return list(
            self._activities.values()
        )

    def list_by_date(
        self,
        report_date: date,
    ) -> list[OperationalActivity]:
        day_start = datetime.combine(
            report_date,
            time.min,
        )

        day_end = day_start + timedelta(days=1)

        activities = []

        for activity in self._activities.values():
            starts_before_day_end = (
                activity.started_at < day_end
            )

            ends_after_day_start = (
                activity.ended_at is None
                or activity.ended_at > day_start
            )

            if (
                starts_before_day_end
                and ends_after_day_start
            ):
                activities.append(activity)

        return activities

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)
from app.operations.daily_reports.results import (
    DailyActivityResult,
    DailyOperationalReportResult,
    DailyWorkOrderResult,
)


@dataclass(frozen=True)
class GetDailyOperationalReportQuery:
    report_date: date


class GetDailyOperationalReport:

    def __init__(
        self,
        work_order_repository,
        activity_repository,
        work_session_repository,
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._activity_repository = (
            activity_repository
        )

        self._work_session_repository = (
            work_session_repository
        )

    def execute(
        self,
        query: GetDailyOperationalReportQuery,
    ) -> DailyOperationalReportResult:

        day_start = datetime.combine(
            query.report_date,
            time.min,
        )

        day_end = (
            day_start
            + timedelta(days=1)
        )

        daily_work_orders = []

        total_activities = 0
        completed_activities = 0
        in_progress_activities = 0
        on_hold_activities = 0
        total_effective_seconds = 0

        work_orders = (
            self._work_order_repository.list_all()
        )

        for work_order in work_orders:

            daily_activities = []

            activities = (
                self._activity_repository
                .list_by_work_order(
                    work_order.code
                )
            )

            for activity in activities:

                sessions = (
                    self._work_session_repository
                    .list_by_activity(
                        activity.code
                    )
                )

                effective_seconds = 0
                session_starts = []
                session_ends = []

                for session in sessions:

                    if session.ended_at is None:
                        continue

                    effective_start = max(
                        session.started_at,
                        day_start,
                    )

                    effective_end = min(
                        session.ended_at,
                        day_end,
                    )

                    if effective_end <= effective_start:
                        continue

                    effective_seconds += int(
                        (
                            effective_end
                            - effective_start
                        ).total_seconds()
                    )

                    session_starts.append(
                        effective_start
                    )

                    session_ends.append(
                        effective_end
                    )

                completed_during_day = (
                    activity.completed_at is not None
                    and day_start
                    <= activity.completed_at
                    < day_end
                )

                has_effective_work = (
                    effective_seconds > 0
                )

                if (
                    not has_effective_work
                    and not completed_during_day
                ):
                    continue

                daily_activity = (
                    DailyActivityResult(
                        activity_code=activity.code,
                        title=activity.title,
                        status=activity.status.value,
                        completion_notes=(
                            activity.completion_notes
                        ),
                        first_started_at=(
                            min(session_starts)
                            if session_starts
                            else None
                        ),
                        last_ended_at=(
                            max(session_ends)
                            if session_ends
                            else None
                        ),
                        effective_seconds=(
                            effective_seconds
                        ),
                    )
                )

                daily_activities.append(
                    daily_activity
                )

                total_activities += 1
                total_effective_seconds += (
                    effective_seconds
                )

                if (
                    activity.status
                    == ActivityStatus.COMPLETED
                ):
                    completed_activities += 1

                elif (
                    activity.status
                    == ActivityStatus.IN_PROGRESS
                ):
                    in_progress_activities += 1

                elif (
                    activity.status
                    == ActivityStatus.ON_HOLD
                ):
                    on_hold_activities += 1

            if not daily_activities:
                continue

            daily_work_orders.append(
                DailyWorkOrderResult(
                    work_order_code=(
                        work_order.code
                    ),
                    title=work_order.title,
                    asset_code=(
                        work_order.asset_code
                    ),
                    activities=(
                        daily_activities
                    ),
                )
            )

        return DailyOperationalReportResult(
            report_date=query.report_date,
            work_orders=daily_work_orders,
            total_work_orders=len(
                daily_work_orders
            ),
            total_activities=total_activities,
            completed_activities=(
                completed_activities
            ),
            in_progress_activities=(
                in_progress_activities
            ),
            on_hold_activities=(
                on_hold_activities
            ),
            effective_seconds=(
                total_effective_seconds
            ),
        )

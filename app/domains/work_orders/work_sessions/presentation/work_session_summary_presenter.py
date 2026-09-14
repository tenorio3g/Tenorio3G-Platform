from collections import defaultdict

from app.domains.work_orders.work_sessions.use_cases.get_work_session_summary import (
    GetWorkSessionSummaryResult,
)

from .work_session_summary_view_model import (
    ActivityWorkSessionSummaryViewModel,
    TechnicianWorkSessionSummaryViewModel,
    WorkSessionItemViewModel,
    WorkSessionSummaryViewModel,
)


class WorkSessionSummaryPresenter:

    @classmethod
    def present(
        cls,
        result: GetWorkSessionSummaryResult,
    ) -> WorkSessionSummaryViewModel:

        grouped = defaultdict(list)

        for item in result.items:
            grouped[
                item.work_session.activity_code
            ].append(
                item
            )

        by_activity = {}

        for activity_code, items in grouped.items():

            sessions = []
            technician_data = {}

            total_minutes = 0
            closed_session_count = 0
            has_active_session = False

            for item in items:

                work_session = (
                    item.work_session
                )

                person = item.person

                duration_minutes = (
                    work_session.duration_minutes
                )

                if duration_minutes is not None:
                    total_minutes += (
                        duration_minutes
                    )

                    closed_session_count += 1
                else:
                    has_active_session = True

                sessions.append(
                    WorkSessionItemViewModel(
                        code=work_session.code,
                        person_code=person.code,
                        person_name=person.name,
                        started_at=(
                            cls._format_datetime(
                                work_session.started_at
                            )
                        ),
                        ended_at=(
                            cls._format_datetime(
                                work_session.ended_at
                            )
                        ),
                        duration_minutes=(
                            duration_minutes
                        ),
                        duration_label=(
                            "En curso"
                            if duration_minutes is None
                            else cls._format_duration(
                                duration_minutes
                            )
                        ),
                        is_active=(
                            work_session.is_active
                        ),
                    )
                )

                if person.code not in technician_data:
                    technician_data[
                        person.code
                    ] = {
                        "person_name": person.name,
                        "total_minutes": 0,
                        "closed_session_count": 0,
                        "has_active_session": False,
                    }

                technician = (
                    technician_data[
                        person.code
                    ]
                )

                if duration_minutes is None:
                    technician[
                        "has_active_session"
                    ] = True
                else:
                    technician[
                        "total_minutes"
                    ] += duration_minutes

                    technician[
                        "closed_session_count"
                    ] += 1

            technicians = [
                TechnicianWorkSessionSummaryViewModel(
                    person_code=person_code,
                    person_name=data[
                        "person_name"
                    ],
                    total_minutes=data[
                        "total_minutes"
                    ],
                    total_duration_label=(
                        cls._format_duration(
                            data[
                                "total_minutes"
                            ]
                        )
                    ),
                    closed_session_count=data[
                        "closed_session_count"
                    ],
                    has_active_session=data[
                        "has_active_session"
                    ],
                )
                for person_code, data
                in technician_data.items()
            ]

            by_activity[
                activity_code
            ] = (
                ActivityWorkSessionSummaryViewModel(
                    activity_code=activity_code,
                    sessions=sessions,
                    technicians=technicians,
                    total_minutes=total_minutes,
                    total_duration_label=(
                        cls._format_duration(
                            total_minutes
                        )
                    ),
                    closed_session_count=(
                        closed_session_count
                    ),
                    has_active_session=(
                        has_active_session
                    ),
                )
            )

        return WorkSessionSummaryViewModel(
            by_activity=by_activity
        )

    @staticmethod
    def _format_datetime(
        value,
    ) -> str | None:

        if value is None:
            return None

        return value.strftime(
            "%d/%m/%Y %H:%M"
        )

    @staticmethod
    def _format_duration(
        minutes: int,
    ) -> str:

        hours, remaining_minutes = divmod(
            minutes,
            60,
        )

        if hours and remaining_minutes:
            return (
                f"{hours} h "
                f"{remaining_minutes} min"
            )

        if hours:
            return f"{hours} h"

        return f"{remaining_minutes} min"
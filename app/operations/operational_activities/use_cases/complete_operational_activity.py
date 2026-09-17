from datetime import datetime

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
)
from app.operations.operational_activities.repositories.operational_activity_repository import (
    OperationalActivityRepository,
)


class CompleteOperationalActivity:
    def __init__(
        self,
        repository: OperationalActivityRepository,
    ):
        self._repository = repository

    def execute(
        self,
        code: str,
        ended_at: datetime,
        result_notes: str = "",
        completed_at: datetime | None = None,
        completed_by_person_code: str = "",
    ) -> OperationalActivity:
        normalized_code = (
            code.strip().upper()
        )

        if not normalized_code:
            raise ValueError(
                "code is required"
            )

        activity = self._repository.get_by_code(
            normalized_code
        )

        if activity is None:
            raise ValueError(
                "operational activity not found"
            )

        normalized_completed_by_person_code = (
            completed_by_person_code.strip().upper()
        )

        if not normalized_completed_by_person_code:
            raise ValueError(
                "completed_by_person_code is required"
            )

        if completed_at is None:
            raise ValueError(
                "completed_at is required"
            )

        activity.complete(
            ended_at=ended_at,
            result_notes=result_notes,
            completed_at=completed_at,
            completed_by_person_code=(
                normalized_completed_by_person_code
            ),
        )

        self._repository.save(activity)

        return activity

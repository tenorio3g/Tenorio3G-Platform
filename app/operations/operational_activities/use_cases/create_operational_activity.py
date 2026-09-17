from datetime import datetime

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
    OperationalActivitySource,
)
from app.operations.operational_activities.repositories.operational_activity_repository import (
    OperationalActivityRepository,
)


class CreateOperationalActivity:
    def __init__(
        self,
        repository: OperationalActivityRepository,
    ):
        self._repository = repository

    def execute(
        self,
        code: str,
        description: str,
        started_at: datetime,
        area: str = "",
        location_description: str = "",
        asset_code: str | None = None,
        work_order_code: str | None = None,
        created_by_person_code: str = "",
    ) -> OperationalActivity:
        normalized_code = (
            code.strip().upper()
        )

        if not normalized_code:
            raise ValueError(
                "code is required"
            )

        normalized_description = (
            description.strip()
        )

        if not normalized_description:
            raise ValueError(
                "description is required"
            )

        normalized_created_by_person_code = (
            created_by_person_code.strip().upper()
        )

        if not normalized_created_by_person_code:
            raise ValueError(
                "created_by_person_code is required"
            )

        existing_activity = (
            self._repository.get_by_code(
                normalized_code
            )
        )

        if existing_activity is not None:
            raise ValueError(
                "operational activity code already exists"
            )

        activity = OperationalActivity(
            code=normalized_code,
            description=normalized_description,
            started_at=started_at,
            area=area,
            location_description=location_description,
            asset_code=asset_code,
            work_order_code=work_order_code,
            source=OperationalActivitySource.MANUAL,
            created_by_person_code=(
                normalized_created_by_person_code
            ),
        )

        self._repository.save(activity)

        return activity

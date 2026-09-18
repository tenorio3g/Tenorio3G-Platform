from datetime import datetime
from uuid import uuid4

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
    OperationalActivitySource,
)
from app.operations.operational_activities.repositories.operational_activity_repository import (
    OperationalActivityRepository,
)


class CreateOperationalActivity:
    MAX_CODE_GENERATION_ATTEMPTS = 10

    def __init__(
        self,
        repository: OperationalActivityRepository,
    ):
        self._repository = repository

    def execute(
        self,
        description: str,
        started_at: datetime,
        area: str = "",
        location_description: str = "",
        asset_code: str | None = None,
        work_order_code: str | None = None,
        created_by_person_code: str = "",
    ) -> OperationalActivity:
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

        code = self._generate_unique_code()

        activity = OperationalActivity(
            code=code,
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

    def _generate_unique_code(
        self,
    ) -> str:
        for _ in range(
            self.MAX_CODE_GENERATION_ATTEMPTS
        ):
            code = (
                "OPA-"
                + uuid4().hex[:8].upper()
            )

            existing_activity = (
                self._repository.get_by_code(
                    code
                )
            )

            if existing_activity is None:
                return code

        raise RuntimeError(
            "unable to generate unique "
            "operational activity code"
        )

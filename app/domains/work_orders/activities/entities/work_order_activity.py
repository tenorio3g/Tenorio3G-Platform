from datetime import datetime

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)


class WorkOrderActivity:

    def __init__(
        self,
        code,
        work_order_code,
        title,
        responsible_person_code,
        description="",
        estimated_minutes=None,
        status=ActivityStatus.PENDING,
        started_at=None,
        completed_at=None,
    ):
        self.code = self._required(
            code,
            "code",
        ).upper()

        self.work_order_code = self._required(
            work_order_code,
            "work_order_code",
        ).upper()

        self.title = self._required(
            title,
            "title",
        )

        self.responsible_person_code = (
            self._required(
                responsible_person_code,
                "responsible_person_code",
            )
        )

        self.description = str(
            description
        ).strip()

        if estimated_minutes is None:
            self.estimated_minutes = None
        else:
            self.estimated_minutes = int(
                estimated_minutes
            )

            if self.estimated_minutes <= 0:
                raise ValueError(
                    "estimated_minutes must be greater than zero"
                )

        if not isinstance(
            status,
            ActivityStatus,
        ):
            raise ValueError(
                "status must be an ActivityStatus"
            )

        self.status = status

        if (
            started_at is not None
            and not isinstance(
                started_at,
                datetime,
            )
        ):
            raise ValueError(
                "started_at must be a datetime"
            )

        if (
            completed_at is not None
            and not isinstance(
                completed_at,
                datetime,
            )
        ):
            raise ValueError(
                "completed_at must be a datetime"
            )

        self.started_at = started_at
        self.completed_at = completed_at

    @staticmethod
    def _required(
        value,
        field_name,
    ) -> str:

        normalized = str(
            value
        ).strip()

        if not normalized:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized

    def start(
        self,
        started_at: datetime,
    ) -> None:

        if self.status != ActivityStatus.PENDING:
            raise ValueError(
                "activity cannot be started from current status"
            )

        if not isinstance(
            started_at,
            datetime,
        ):
            raise ValueError(
                "started_at must be a datetime"
            )

        self.status = (
            ActivityStatus.IN_PROGRESS
        )

        self.started_at = started_at


    def complete(
        self,
        completed_at: datetime,
    ) -> None:

        if (
            self.status
            != ActivityStatus.IN_PROGRESS
        ):
            raise ValueError(
                "activity cannot be completed from current status"
            )

        if not isinstance(
            completed_at,
            datetime,
        ):
            raise ValueError(
                "completed_at must be a datetime"
            )

        if (
            self.started_at is not None
            and completed_at < self.started_at
        ):
            raise ValueError(
                "completed_at cannot be before started_at"
            )

        self.status = (
            ActivityStatus.COMPLETED
        )

        self.completed_at = completed_at


    @property
    def actual_minutes(
        self,
    ) -> int | None:

        if (
            self.started_at is None
            or self.completed_at is None
        ):
            return None

        duration = (
            self.completed_at
            - self.started_at
        )

        return int(
            duration.total_seconds()
            // 60
        )
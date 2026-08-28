from __future__ import annotations

from datetime import datetime

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


class WorkSession:

    def __init__(
        self,
        code: str,
        work_order_code: str,
        activity_code: str,
        person_code: str,
        started_at: datetime,
        source: WorkSessionSource,
        created_at: datetime,
        created_by_person_code: str,
        ended_at: datetime | None = None,
    ):

        self.code = self._normalize_required_code(
            code,
            "code",
        )

        self.work_order_code = (
            self._normalize_required_code(
                work_order_code,
                "work_order_code",
            )
        )

        self.activity_code = (
            self._normalize_required_code(
                activity_code,
                "activity_code",
            )
        )

        self.person_code = (
            self._normalize_required_code(
                person_code,
                "person_code",
            )
        )

        self.created_by_person_code = (
            self._normalize_required_code(
                created_by_person_code,
                "created_by_person_code",
            )
        )

        if not isinstance(
            started_at,
            datetime,
        ):
            raise ValueError(
                "started_at must be datetime"
            )

        if not isinstance(
            created_at,
            datetime,
        ):
            raise ValueError(
                "created_at must be datetime"
            )

        if not isinstance(
            source,
            WorkSessionSource,
        ):
            raise ValueError(
                "invalid work session source"
            )

        if (
            ended_at is not None
            and not isinstance(
                ended_at,
                datetime,
            )
        ):
            raise ValueError(
                "ended_at must be datetime"
            )

        if (
            ended_at is not None
            and ended_at < started_at
        ):
            raise ValueError(
                "end cannot be before start"
            )

        self.started_at = started_at
        self.ended_at = ended_at
        self.source = source
        self.created_at = created_at

    @property
    def is_active(
        self,
    ) -> bool:

        return self.ended_at is None

    @property
    def duration_minutes(
        self,
    ) -> int | None:

        if self.ended_at is None:
            return None

        duration = (
            self.ended_at
            - self.started_at
        )

        return int(
            duration.total_seconds()
            / 60
        )

    def end(
        self,
        ended_at: datetime,
    ) -> None:

        if not self.is_active:
            raise ValueError(
                "work session already ended"
            )

        if not isinstance(
            ended_at,
            datetime,
        ):
            raise ValueError(
                "ended_at must be datetime"
            )

        if ended_at < self.started_at:
            raise ValueError(
                "end cannot be before start"
            )

        self.ended_at = ended_at

    def correct(
        self,
        started_at: datetime,
        ended_at: datetime,
    ) -> None:

        if self.source != WorkSessionSource.MANUAL:
            raise ValueError(
                "only manual work sessions can be corrected"
            )

        if not isinstance(
            started_at,
            datetime,
        ):
            raise ValueError(
                "started_at must be datetime"
            )

        if not isinstance(
            ended_at,
            datetime,
        ):
            raise ValueError(
                "ended_at must be datetime"
            )

        if ended_at < started_at:
            raise ValueError(
                "end cannot be before start"
            )

        self.started_at = started_at
        self.ended_at = ended_at

    @staticmethod
    def _normalize_required_code(
        value: str,
        field_name: str,
    ) -> str:

        normalized_value = str(
            value
        ).strip().upper()

        if not normalized_value:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized_value

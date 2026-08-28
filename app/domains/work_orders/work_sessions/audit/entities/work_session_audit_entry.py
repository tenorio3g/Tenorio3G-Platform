from datetime import datetime

from app.domains.work_orders.work_sessions.audit.value_objects import (
    WorkSessionAuditEventType,
)


class WorkSessionAuditEntry:

    def __init__(
        self,
        work_session_code: str,
        event_type: WorkSessionAuditEventType,
        reason: str,
        actor_person_code: str,
        occurred_at: datetime,
        previous_started_at: datetime | None = None,
        previous_ended_at: datetime | None = None,
        new_started_at: datetime | None = None,
        new_ended_at: datetime | None = None,
    ):

        self.work_session_code = (
            self._normalize_required_code(
                work_session_code,
                "work_session_code",
            )
        )

        self.actor_person_code = (
            self._normalize_required_code(
                actor_person_code,
                "actor_person_code",
            )
        )

        self.reason = self._clean_reason(
            reason
        )

        if not isinstance(
            event_type,
            WorkSessionAuditEventType,
        ):
            raise ValueError(
                "invalid audit event type"
            )

        if not isinstance(
            occurred_at,
            datetime,
        ):
            raise ValueError(
                "occurred_at must be datetime"
            )

        self.event_type = event_type
        self.occurred_at = occurred_at

        self.previous_started_at = (
            previous_started_at
        )

        self.previous_ended_at = (
            previous_ended_at
        )

        self.new_started_at = (
            new_started_at
        )

        self.new_ended_at = (
            new_ended_at
        )

        self._validate_event_data()

    def _validate_event_data(
        self,
    ) -> None:

        if (
            self.event_type
            == WorkSessionAuditEventType.CORRECTED
        ):

            correction_values = (
                self.previous_started_at,
                self.previous_ended_at,
                self.new_started_at,
                self.new_ended_at,
            )

            if any(
                value is None
                for value in correction_values
            ):
                raise ValueError(
                    "correction time values are required"
                )

            for value in correction_values:

                if not isinstance(
                    value,
                    datetime,
                ):
                    raise ValueError(
                        "correction time values "
                        "must be datetime"
                    )

            if (
                self.new_ended_at
                < self.new_started_at
            ):
                raise ValueError(
                    "new end cannot be before new start"
                )

    @staticmethod
    def _normalize_required_code(
        value,
        field_name: str,
    ) -> str:

        normalized = str(
            value
        ).strip().upper()

        if not normalized:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized

    @staticmethod
    def _clean_reason(
        value,
    ) -> str:

        reason = str(
            value
        ).strip()

        if not reason:
            raise ValueError(
                "reason is required"
            )

        return reason

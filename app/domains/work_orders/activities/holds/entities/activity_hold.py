from datetime import datetime

from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)


class ActivityHold:

    def __init__(
        self,
        code: str,
        activity_code: str,
        reason: ActivityHoldReason,
        observations: str,
        held_at: datetime,
        held_by_person_code: str,
        resumed_at: datetime | None = None,
        resumed_by_person_code: str | None = None,
    ):

        normalized_code = str(
            code
        ).strip().upper()

        if not normalized_code:
            raise ValueError(
                "code is required"
            )

        normalized_activity_code = str(
            activity_code
        ).strip().upper()

        if not normalized_activity_code:
            raise ValueError(
                "activity_code is required"
            )

        if not isinstance(
            reason,
            ActivityHoldReason,
        ):
            raise ValueError(
                "reason must be ActivityHoldReason"
            )

        if not isinstance(
            held_at,
            datetime,
        ):
            raise ValueError(
                "held_at must be datetime"
            )

        normalized_held_by_person_code = str(
            held_by_person_code
        ).strip().upper()

        if not normalized_held_by_person_code:
            raise ValueError(
                "held_by_person_code is required"
            )

        normalized_observations = str(
            observations or ""
        ).strip()

        if resumed_at is not None:

            if not isinstance(
                resumed_at,
                datetime,
            ):
                raise ValueError(
                    "resumed_at must be datetime"
                )

            if resumed_at < held_at:
                raise ValueError(
                    "resumed_at cannot be before held_at"
                )

        normalized_resumed_by_person_code = None

        if resumed_by_person_code is not None:

            normalized_resumed_by_person_code = str(
                resumed_by_person_code
            ).strip().upper()

            if not normalized_resumed_by_person_code:
                raise ValueError(
                    "resumed_by_person_code is required"
                )

        if (
            resumed_at is None
            and normalized_resumed_by_person_code
            is not None
        ):
            raise ValueError(
                "resumed_at is required when "
                "resumed_by_person_code is provided"
            )

        if (
            resumed_at is not None
            and normalized_resumed_by_person_code
            is None
        ):
            raise ValueError(
                "resumed_by_person_code is required"
            )

        self.code = normalized_code

        self.activity_code = (
            normalized_activity_code
        )

        self.reason = reason

        self.observations = (
            normalized_observations
        )

        self.held_at = held_at

        self.held_by_person_code = (
            normalized_held_by_person_code
        )

        self.resumed_at = resumed_at

        self.resumed_by_person_code = (
            normalized_resumed_by_person_code
        )


    @property
    def is_active(
        self,
    ) -> bool:

        return self.resumed_at is None


    def resume(
        self,
        resumed_at: datetime,
        resumed_by_person_code: str,
    ) -> None:

        if not self.is_active:
            raise ValueError(
                "activity hold is already resumed"
            )

        if not isinstance(
            resumed_at,
            datetime,
        ):
            raise ValueError(
                "resumed_at must be datetime"
            )

        if resumed_at < self.held_at:
            raise ValueError(
                "resumed_at cannot be before held_at"
            )

        normalized_person_code = str(
            resumed_by_person_code
        ).strip().upper()

        if not normalized_person_code:
            raise ValueError(
                "resumed_by_person_code is required"
            )

        self.resumed_at = resumed_at

        self.resumed_by_person_code = (
            normalized_person_code
        )

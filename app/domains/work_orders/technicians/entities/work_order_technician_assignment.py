from datetime import datetime


class WorkOrderTechnicianAssignment:

    def __init__(
        self,
        work_order_code,
        person_code,
        assigned_at,
        unassigned_at=None,
    ):
        self.work_order_code = self._required(
            work_order_code,
            "work_order_code",
        ).upper()

        self.person_code = self._required(
            person_code,
            "person_code",
        )

        if not isinstance(
            assigned_at,
            datetime,
        ):
            raise ValueError(
                "assigned_at must be a datetime"
            )

        self.assigned_at = assigned_at

        if (
            unassigned_at is not None
            and not isinstance(
                unassigned_at,
                datetime,
            )
        ):
            raise ValueError(
                "unassigned_at must be a datetime or None"
            )

        if (
            unassigned_at is not None
            and unassigned_at < assigned_at
        ):
            raise ValueError(
                "unassigned_at cannot be before assigned_at"
            )

        self.unassigned_at = unassigned_at

    @property
    def is_active(self) -> bool:
        return self.unassigned_at is None

    def unassign(
        self,
        unassigned_at: datetime,
    ) -> None:

        if not isinstance(
            unassigned_at,
            datetime,
        ):
            raise ValueError(
                "unassigned_at must be a datetime"
            )

        if not self.is_active:
            raise ValueError(
                "technician assignment is already inactive"
            )

        if unassigned_at < self.assigned_at:
            raise ValueError(
                "unassigned_at cannot be before assigned_at"
            )

        self.unassigned_at = unassigned_at

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
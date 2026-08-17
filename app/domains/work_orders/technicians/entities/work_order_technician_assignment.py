from datetime import datetime


class WorkOrderTechnicianAssignment:

    def __init__(
        self,
        work_order_code,
        person_code,
        assigned_at,
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
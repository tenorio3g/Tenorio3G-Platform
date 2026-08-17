from datetime import datetime


class WorkOrderSparePartUsage:

    def __init__(
        self,
        work_order_code,
        spare_part_code,
        quantity,
        used_at,
        unit_cost=0,
        observations="",
    ):
        self.work_order_code = self._required(
            work_order_code,
            "work_order_code",
        ).upper()

        self.spare_part_code = self._required(
            spare_part_code,
            "spare_part_code",
        )

        try:
            self.quantity = float(
                quantity
            )
        except (TypeError, ValueError):
            raise ValueError(
                "quantity must be a valid number"
            )

        if self.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero"
            )

        try:
            self.unit_cost = float(
                unit_cost or 0
            )
        except (TypeError, ValueError):
            raise ValueError(
                "unit_cost must be a valid number"
            )

        if self.unit_cost < 0:
            raise ValueError(
                "unit_cost cannot be negative"
            )

        if not isinstance(
            used_at,
            datetime,
        ):
            raise ValueError(
                "used_at must be a datetime"
            )

        self.used_at = used_at

        self.observations = str(
            observations or ""
        ).strip()

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

    @property
    def total_cost(
        self,
    ) -> float:

        return (
            self.quantity
            * self.unit_cost
        )
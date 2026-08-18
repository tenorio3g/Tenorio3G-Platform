from datetime import datetime

from app.domains.work_orders.tools.value_objects import (
    ToolUsageStatus,
)


class WorkOrderToolUsage:

    def __init__(
        self,
        usage_id,
        work_order_code,
        tool_code,
        tool_name,
        quantity,
        issued_at,
        observations="",
        status=ToolUsageStatus.ISSUED,
        returned_at=None,
    ):  
        self.usage_id = self._required(
            usage_id,
            "usage_id",
        ).upper()
        
        self.work_order_code = self._required(
            work_order_code,
            "work_order_code",
        ).upper()

        self.tool_code = self._required(
            tool_code,
            "tool_code",
        )

        self.tool_name = self._required(
            tool_name,
            "tool_name",
        )

        try:
            self.quantity = int(
                quantity
            )
        except (TypeError, ValueError):
            raise ValueError(
                "quantity must be a valid integer"
            )

        if self.quantity <= 0:
            raise ValueError(
                "quantity must be greater than zero"
            )

        if not isinstance(
            issued_at,
            datetime,
        ):
            raise ValueError(
                "issued_at must be a datetime"
            )

        if not isinstance(
            status,
            ToolUsageStatus,
        ):
            raise ValueError(
                "status must be a ToolUsageStatus"
            )

        if (
            returned_at is not None
            and not isinstance(
                returned_at,
                datetime,
            )
        ):
            raise ValueError(
                "returned_at must be a datetime"
            )

        self.issued_at = issued_at
        self.returned_at = returned_at
        self.status = status

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

    def return_tool(
        self,
        returned_at: datetime,
    ) -> None:

        if self.status != ToolUsageStatus.ISSUED:
            raise ValueError(
                "tool usage cannot be returned from current status"
            )

        if not isinstance(
            returned_at,
            datetime,
        ):
            raise ValueError(
                "returned_at must be a datetime"
            )

        if returned_at < self.issued_at:
            raise ValueError(
                "returned_at cannot be before issued_at"
            )

        self.returned_at = returned_at
        self.status = ToolUsageStatus.RETURNED


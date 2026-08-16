from datetime import datetime

from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)


class WorkOrder:

    def __init__(
        self,
        code,
        title,
        description,
        work_type,
        priority,
        asset_code,
        requester_person_code,
        supervisor_person_code,
        created_at,
        status=WorkOrderStatus.CREATED,
    ):
        self.code = self._required(
            code,
            "code",
        ).upper()

        self.title = self._required(
            title,
            "title",
        )

        self.description = str(
            description
        ).strip()

        self.work_type = self._required(
            work_type,
            "work_type",
        ).upper()

        self.priority = self._required(
            priority,
            "priority",
        ).upper()

        self.asset_code = self._required(
            asset_code,
            "asset_code",
        ).upper()

        self.requester_person_code = (
            self._required(
                requester_person_code,
                "requester_person_code",
            ).upper()
        )

        self.supervisor_person_code = (
            self._required(
                supervisor_person_code,
                "supervisor_person_code",
            ).upper()
        )

        if not isinstance(
            created_at,
            datetime,
        ):
            raise ValueError(
                "created_at must be a datetime"
            )

        self.created_at = created_at

        if not isinstance(
            status,
            WorkOrderStatus,
        ):
            raise ValueError(
                "status must be a WorkOrderStatus"
            )

        self.status = status

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

    def assign(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.CREATED:
            raise ValueError(
                "work order cannot be assigned from current status"
            )

        self.status = WorkOrderStatus.ASSIGNED


    def start(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.ASSIGNED:
            raise ValueError(
                "work order cannot be started from current status"
            )

        self.status = WorkOrderStatus.IN_PROGRESS


    def hold(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.IN_PROGRESS:
            raise ValueError(
                "work order cannot be placed on hold from current status"
            )

        self.status = WorkOrderStatus.ON_HOLD


    def resume(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.ON_HOLD:
            raise ValueError(
                "work order cannot be resumed from current status"
            )

        self.status = WorkOrderStatus.IN_PROGRESS


    def complete(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.IN_PROGRESS:
            raise ValueError(
                "work order cannot be completed from current status"
            )

        self.status = WorkOrderStatus.COMPLETED


    def close(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.COMPLETED:
            raise ValueError(
                "work order cannot be closed from current status"
            )

        self.status = WorkOrderStatus.CLOSED


    def cancel(
        self,
    ) -> None:

        if self.status in (
            WorkOrderStatus.COMPLETED,
            WorkOrderStatus.CLOSED,
            WorkOrderStatus.CANCELLED,
        ):
            raise ValueError(
                "work order cannot be cancelled from current status"
            )

        self.status = WorkOrderStatus.CANCELLED
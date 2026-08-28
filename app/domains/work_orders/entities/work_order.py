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
        requester_name=None,
        requester_phone=None,
        requester_area=None,
        location_description=None,
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

        self.asset_code = self._optional_code(
            asset_code
        )

        self.requester_person_code = (
            self._optional_code(
                requester_person_code
            )
        )

        self.supervisor_person_code = (
            self._optional_code(
                supervisor_person_code
            )
        )

        self.requester_name = (
            self._optional_text(
                requester_name
            )
        )

        self.requester_phone = (
            self._optional_text(
                requester_phone
            )
        )

        self.requester_area = (
            self._optional_text(
                requester_area
            )
        )

        self.location_description = (
            self._optional_text(
                location_description
            )
        )

        self._validate_requester()

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

    def _validate_requester(
        self,
    ) -> None:

        if self.requester_person_code:
            return

        if not self.requester_name:
            raise ValueError(
                "requester name is required"
            )

        if not self.requester_phone:
            raise ValueError(
                "requester phone is required"
            )

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

    @staticmethod
    def _optional_code(
        value,
    ) -> str | None:

        if value is None:
            return None

        normalized = str(
            value
        ).strip()

        if not normalized:
            return None

        return normalized.upper()

    @staticmethod
    def _optional_text(
        value,
    ) -> str | None:

        if value is None:
            return None

        normalized = str(
            value
        ).strip()

        if not normalized:
            return None

        return normalized

    def approve(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.CREATED:
            raise ValueError(
                "work order cannot be approved from current status"
            )

        self.status = WorkOrderStatus.APPROVED


    def assign(
        self,
    ) -> None:

        if self.status != WorkOrderStatus.APPROVED:
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

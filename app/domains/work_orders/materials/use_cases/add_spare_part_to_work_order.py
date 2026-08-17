from dataclasses import dataclass
from datetime import datetime

from app.domains.assets.spare_parts.repositories import (
    SparePartRepository,
)

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.repositories import (
    WorkOrderSparePartUsageRepository,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class AddSparePartToWorkOrderCommand:
    work_order_code: str
    spare_part_code: str
    quantity: float
    used_at: datetime
    unit_cost: float = 0
    observations: str = ""


@dataclass(frozen=True)
class AddSparePartToWorkOrderResult:
    usage: WorkOrderSparePartUsage


class AddSparePartToWorkOrder:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        spare_part_repository: SparePartRepository,
        usage_repository: WorkOrderSparePartUsageRepository,
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._spare_part_repository = (
            spare_part_repository
        )

        self._usage_repository = (
            usage_repository
        )

    def execute(
        self,
        command: AddSparePartToWorkOrderCommand,
    ) -> AddSparePartToWorkOrderResult:

        work_order_code = str(
            command.work_order_code
        ).strip().upper()

        spare_part_code = str(
            command.spare_part_code
        ).strip()

        work_order = (
            self._work_order_repository
            .get_by_code(
                work_order_code
            )
        )

        if work_order is None:
            raise ValueError(
                "work order not found"
            )

        spare_part = (
            self._spare_part_repository
            .get_spare_part_by_code(
                spare_part_code
            )
        )

        if spare_part is None:
            raise ValueError(
                "spare part not found"
            )

        usage = WorkOrderSparePartUsage(
            work_order_code=(
                work_order.code
            ),
            spare_part_code=(
                spare_part.code
            ),
            quantity=command.quantity,
            unit_cost=command.unit_cost,
            used_at=command.used_at,
            observations=command.observations,
        )

        self._usage_repository.save(
            usage
        )

        return AddSparePartToWorkOrderResult(
            usage=usage
        )
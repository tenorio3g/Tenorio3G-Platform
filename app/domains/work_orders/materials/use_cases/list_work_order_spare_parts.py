from dataclasses import dataclass

from app.domains.assets.spare_parts.entities import (
    SparePart,
)

from app.domains.assets.spare_parts.repositories import (
    SparePartRepository,
)

from app.domains.work_orders.materials.entities import (
    WorkOrderSparePartUsage,
)

from app.domains.work_orders.materials.repositories import (
    WorkOrderSparePartUsageRepository,
)


@dataclass(frozen=True)
class WorkOrderSparePartItem:
    usage: WorkOrderSparePartUsage
    spare_part: SparePart


@dataclass(frozen=True)
class ListWorkOrderSparePartsQuery:
    work_order_code: str


@dataclass(frozen=True)
class ListWorkOrderSparePartsResult:
    items: list[WorkOrderSparePartItem]


class ListWorkOrderSpareParts:

    def __init__(
        self,
        usage_repository: WorkOrderSparePartUsageRepository,
        spare_part_repository: SparePartRepository,
    ):
        self._usage_repository = (
            usage_repository
        )

        self._spare_part_repository = (
            spare_part_repository
        )

    def execute(
        self,
        query: ListWorkOrderSparePartsQuery,
    ) -> ListWorkOrderSparePartsResult:

        work_order_code = str(
            query.work_order_code
        ).strip().upper()

        usages = (
            self._usage_repository
            .list_by_work_order(
                work_order_code
            )
        )

        items = []

        for usage in usages:

            spare_part = (
                self._spare_part_repository
                .get_spare_part_by_code(
                    usage.spare_part_code
                )
            )

            if spare_part is None:
                continue

            items.append(
                WorkOrderSparePartItem(
                    usage=usage,
                    spare_part=spare_part,
                )
            )

        return ListWorkOrderSparePartsResult(
            items=items
        )
from dataclasses import dataclass

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.repositories import (
    WorkOrderEvidenceRepository,
)


@dataclass(frozen=True)
class ListWorkOrderEvidenceQuery:
    work_order_code: str


@dataclass(frozen=True)
class ListWorkOrderEvidenceResult:
    items: list[WorkOrderEvidence]


class ListWorkOrderEvidence:

    def __init__(
        self,
        repository: WorkOrderEvidenceRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: ListWorkOrderEvidenceQuery,
    ) -> ListWorkOrderEvidenceResult:

        work_order_code = str(
            query.work_order_code
        ).strip().upper()

        items = (
            self._repository
            .list_by_work_order(
                work_order_code
            )
        )

        return ListWorkOrderEvidenceResult(
            items=items
        )
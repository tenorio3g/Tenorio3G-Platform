from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from .work_order_evidence_repository import (
    WorkOrderEvidenceRepository,
)


class InMemoryWorkOrderEvidenceRepository(
    WorkOrderEvidenceRepository,
):

    def __init__(
        self,
    ):
        self._items: dict[
            str,
            WorkOrderEvidence,
        ] = {}

    def save(
        self,
        evidence: WorkOrderEvidence,
    ) -> None:

        self._items[
            evidence.evidence_id
        ] = evidence

    def get_by_id(
        self,
        evidence_id: str,
    ) -> WorkOrderEvidence | None:

        normalized_id = str(
            evidence_id
        ).strip().upper()

        return self._items.get(
            normalized_id
        )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderEvidence]:

        normalized_code = str(
            work_order_code
        ).strip().upper()

        return [
            evidence
            for evidence
            in self._items.values()
            if evidence.work_order_code
            == normalized_code
        ]

    def delete(
        self,
        evidence_id: str,
    ) -> None:

        normalized_id = str(
            evidence_id
        ).strip().upper()

        self._items.pop(
            normalized_id,
            None,
        )
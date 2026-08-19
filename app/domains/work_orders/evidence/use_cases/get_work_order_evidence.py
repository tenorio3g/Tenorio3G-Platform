from dataclasses import dataclass

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.repositories import (
    WorkOrderEvidenceRepository,
)


@dataclass(frozen=True)
class GetWorkOrderEvidenceQuery:
    evidence_id: str


@dataclass(frozen=True)
class GetWorkOrderEvidenceResult:
    evidence: WorkOrderEvidence


class GetWorkOrderEvidence:

    def __init__(
        self,
        repository: WorkOrderEvidenceRepository,
    ):
        self._repository = repository

    def execute(
        self,
        query: GetWorkOrderEvidenceQuery,
    ) -> GetWorkOrderEvidenceResult:

        evidence_id = str(
            query.evidence_id
        ).strip().upper()

        evidence = (
            self._repository
            .get_by_id(
                evidence_id
            )
        )

        if evidence is None:
            raise ValueError(
                "evidence not found"
            )

        return GetWorkOrderEvidenceResult(
            evidence=evidence
        )
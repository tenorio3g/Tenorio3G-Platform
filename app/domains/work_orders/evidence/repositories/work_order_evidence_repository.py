from abc import ABC, abstractmethod

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)


class WorkOrderEvidenceRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        evidence: WorkOrderEvidence,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(
        self,
        evidence_id: str,
    ) -> WorkOrderEvidence | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderEvidence]:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        evidence_id: str,
    ) -> None:
        raise NotImplementedError
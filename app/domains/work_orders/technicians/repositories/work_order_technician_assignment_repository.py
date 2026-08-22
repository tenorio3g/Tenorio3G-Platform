from abc import ABC, abstractmethod
from datetime import datetime

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)


class WorkOrderTechnicianAssignmentRepository(
    ABC,
):

    @abstractmethod
    def save(
        self,
        assignment: WorkOrderTechnicianAssignment,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        work_order_code: str,
        person_code: str,
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[WorkOrderTechnicianAssignment]:
        raise NotImplementedError

    @abstractmethod
    def unassign(
        self,
        work_order_code: str,
        person_code: str,
        unassigned_at: datetime,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def reactivate(
        self,
        work_order_code: str,
        person_code: str,
        assigned_at: datetime,
    ) -> WorkOrderTechnicianAssignment:
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        work_order_code: str,
        person_code: str,
    ) -> None:
        raise NotImplementedError
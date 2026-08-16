from dataclasses import dataclass
from datetime import datetime

from app.domains.assets.repositories import (
    AssetRepository,
)

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class CreateWorkOrderCommand:
    code: str
    title: str
    description: str
    work_type: str
    priority: str
    asset_code: str
    requester_person_code: str
    supervisor_person_code: str
    created_at: datetime


@dataclass(frozen=True)
class CreateWorkOrderResult:
    work_order: WorkOrder


class CreateWorkOrder:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        asset_repository: AssetRepository,
        person_repository: PersonRepository,
    ):
        self._work_order_repository = (
            work_order_repository
        )

        self._asset_repository = (
            asset_repository
        )

        self._person_repository = (
            person_repository
        )

    def execute(
        self,
        command: CreateWorkOrderCommand,
    ) -> CreateWorkOrderResult:

        normalized_code = str(
            command.code
        ).strip().upper()

        existing = (
            self._work_order_repository
            .get_by_code(
                normalized_code
            )
        )

        if existing is not None:
            raise ValueError(
                "work order already exists"
            )

        asset = (
            self._asset_repository
            .find_by_code(
                command.asset_code
            )
        )

        if asset is None:
            raise ValueError(
                "asset not found"
            )

        requester = (
            self._person_repository
            .get_by_code(
                command.requester_person_code
            )
        )

        if requester is None:
            raise ValueError(
                "requester not found"
            )

        if not requester.is_active:
            raise ValueError(
                "requester is inactive"
            )

        supervisor = (
            self._person_repository
            .get_by_code(
                command.supervisor_person_code
            )
        )

        if supervisor is None:
            raise ValueError(
                "supervisor not found"
            )

        if not supervisor.is_active:
            raise ValueError(
                "supervisor is inactive"
            )

        work_order = WorkOrder(
            code=normalized_code,
            title=command.title,
            description=command.description,
            work_type=command.work_type,
            priority=command.priority,
            asset_code=command.asset_code,
            requester_person_code=requester.code,
            supervisor_person_code=supervisor.code,
            created_at=command.created_at,
        )

        self._work_order_repository.save(
            work_order
        )

        return CreateWorkOrderResult(
            work_order=work_order
        )
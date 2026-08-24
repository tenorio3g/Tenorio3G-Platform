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

from app.foundation.timeline.engine.use_cases import (
    RecordTimelineEvent,
    RecordTimelineEventCommand,
)


@dataclass(frozen=True)
class CreateWorkOrderCommand:
    code: str
    title: str
    description: str
    work_type: str
    priority: str
    asset_code: str | None
    requester_person_code: str | None
    supervisor_person_code: str | None
    created_at: datetime

    requester_name: str | None = None
    requester_phone: str | None = None
    requester_area: str | None = None
    location_description: str | None = None


@dataclass(frozen=True)
class CreateWorkOrderResult:
    work_order: WorkOrder


class CreateWorkOrder:

    def __init__(
        self,
        work_order_repository: WorkOrderRepository,
        asset_repository: AssetRepository,
        person_repository: PersonRepository,
        record_timeline_event: RecordTimelineEvent | None = None,
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

        self._record_timeline_event = (
            record_timeline_event
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

        asset_code = self._optional_code(
            command.asset_code
        )

        requester_person_code = (
            self._optional_code(
                command.requester_person_code
            )
        )

        supervisor_person_code = (
            self._optional_code(
                command.supervisor_person_code
            )
        )

        requester = None
        supervisor = None

        # ====================================================
        # ASSET
        # ====================================================

        if asset_code is not None:

            asset = (
                self._asset_repository
                .find_by_code(
                    asset_code
                )
            )

            if asset is None:
                raise ValueError(
                    "asset not found"
                )

        # ====================================================
        # REQUESTER
        # ====================================================

        if requester_person_code is not None:

            requester = (
                self._person_repository
                .get_by_code(
                    requester_person_code
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

            requester_name = (
                requester.name
            )

            requester_phone = (
                self._optional_text(
                    command.requester_phone
                )
            )

            requester_area = (
                self._optional_text(
                    command.requester_area
                )
            )

        else:

            requester_name = (
                self._optional_text(
                    command.requester_name
                )
            )

            requester_phone = (
                self._optional_text(
                    command.requester_phone
                )
            )

            requester_area = (
                self._optional_text(
                    command.requester_area
                )
            )

        # ====================================================
        # SUPERVISOR
        # ====================================================

        if supervisor_person_code is not None:

            supervisor = (
                self._person_repository
                .get_by_code(
                    supervisor_person_code
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

        # ====================================================
        # ENTITY
        # ====================================================

        work_order = WorkOrder(
            code=normalized_code,
            title=command.title,
            description=command.description,
            work_type=command.work_type,
            priority=command.priority,
            asset_code=asset_code,
            requester_person_code=(
                requester_person_code
            ),
            supervisor_person_code=(
                supervisor_person_code
            ),
            created_at=command.created_at,
            requester_name=(
                requester_name
            ),
            requester_phone=(
                requester_phone
            ),
            requester_area=(
                requester_area
            ),
            location_description=(
                command.location_description
            ),
        )

        self._work_order_repository.save(
            work_order
        )

        # ====================================================
        # TIMELINE
        # ====================================================

        if (
            self._record_timeline_event
            is not None
        ):

            self._record_timeline_event.execute(
                RecordTimelineEventCommand(
                    entity_type="WORK_ORDER",
                    entity_code=work_order.code,
                    event_type=(
                        "WORK_ORDER_CREATED"
                    ),
                    title=(
                        "Orden de trabajo creada"
                    ),
                    actor_person_code=(
                        requester.code
                        if requester
                        else None
                    ),
                    actor_name=(
                        requester.name
                        if requester
                        else work_order.requester_name
                    ),
                    occurred_at=(
                        command.created_at
                    ),
                    description=(
                        work_order.description
                    ),
                    reference_type=(
                        "WORK_ORDER"
                    ),
                    reference_code=(
                        work_order.code
                    ),
                )
            )

        return CreateWorkOrderResult(
            work_order=work_order
        )

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

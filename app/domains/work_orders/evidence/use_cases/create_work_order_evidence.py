from dataclasses import dataclass
from datetime import datetime

from app.domains.identity.people.repositories import (
    PersonRepository,
)

from app.domains.work_orders.activities.repositories import (
    WorkOrderActivityRepository,
)

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.repositories import (
    WorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)

from app.domains.work_orders.repositories import (
    WorkOrderRepository,
)


@dataclass(frozen=True)
class CreateWorkOrderEvidenceCommand:
    evidence_id: str
    work_order_code: str
    title: str
    evidence_type: EvidenceType
    file_name: str
    registered_by_person_code: str
    created_at: datetime
    description: str = ""
    activity_code: str | None = None


@dataclass(frozen=True)
class CreateWorkOrderEvidenceResult:
    evidence: WorkOrderEvidence


class CreateWorkOrderEvidence:

    def __init__(
        self,
        evidence_repository: WorkOrderEvidenceRepository,
        work_order_repository: WorkOrderRepository,
        person_repository: PersonRepository,
        activity_repository: WorkOrderActivityRepository,
    ):
        self._evidence_repository = (
            evidence_repository
        )

        self._work_order_repository = (
            work_order_repository
        )

        self._person_repository = (
            person_repository
        )

        self._activity_repository = (
            activity_repository
        )

    def execute(
        self,
        command: CreateWorkOrderEvidenceCommand,
    ) -> CreateWorkOrderEvidenceResult:

        evidence_id = str(
            command.evidence_id
        ).strip().upper()

        work_order_code = str(
            command.work_order_code
        ).strip().upper()

        existing = (
            self._evidence_repository
            .get_by_id(
                evidence_id
            )
        )

        if existing is not None:
            raise ValueError(
                "evidence already exists"
            )

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

        person = (
            self._person_repository
            .get_by_code(
                command.registered_by_person_code
            )
        )

        if person is None:
            raise ValueError(
                "registered person not found"
            )

        if not person.is_active:
            raise ValueError(
                "registered person is inactive"
            )

        activity_code = None

        if (
            command.activity_code is not None
            and str(command.activity_code).strip()
        ):
            activity_code = str(
                command.activity_code
            ).strip().upper()

            activity = (
                self._activity_repository
                .get_by_code(
                    activity_code
                )
            )

            if activity is None:
                raise ValueError(
                    "activity not found"
                )

            if (
                activity.work_order_code
                != work_order.code
            ):
                raise ValueError(
                    "activity does not belong to work order"
                )

        evidence = WorkOrderEvidence(
            evidence_id=evidence_id,
            work_order_code=work_order.code,
            title=command.title,
            evidence_type=command.evidence_type,
            file_name=command.file_name,
            registered_by_person_code=person.code,
            created_at=command.created_at,
            description=command.description,
            activity_code=activity_code,
        )

        self._evidence_repository.save(
            evidence
        )

        return CreateWorkOrderEvidenceResult(
            evidence=evidence
        )
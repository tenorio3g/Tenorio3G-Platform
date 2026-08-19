from datetime import datetime
from types import SimpleNamespace

import pytest

from app.domains.work_orders.activities.entities import (
    WorkOrderActivity,
)

from app.domains.work_orders.activities.repositories import (
    InMemoryWorkOrderActivityRepository,
)

from app.domains.work_orders.evidence.repositories import (
    InMemoryWorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.use_cases import (
    CreateWorkOrderEvidence,
    CreateWorkOrderEvidenceCommand,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)

from app.domains.work_orders.entities import (
    WorkOrder,
)

from app.domains.work_orders.repositories import (
    InMemoryWorkOrderRepository,
)


class FakePersonRepository:

    def __init__(
        self,
    ):
        self._people = {}

    def save(
        self,
        person,
    ):
        self._people[
            person.code
        ] = person

    def get_by_code(
        self,
        code,
    ):
        return self._people.get(
            str(code).strip()
        )


def create_work_order():

    return WorkOrder(
        code="WO-001",
        title="Orden de prueba",
        description="Prueba Evidence.",
        work_type="CORRECTIVE",
        priority="HIGH",
        asset_code="ASSET-001",
        requester_person_code="P-001",
        supervisor_person_code="P-002",
        created_at=datetime(
            2026,
            8,
            18,
            8,
            0,
        ),
    )


def create_command(
    activity_code="ACT-001",
):

    return CreateWorkOrderEvidenceCommand(
        evidence_id="EVID-001",
        work_order_code="WO-001",
        title="Foto antes",
        evidence_type=(
            EvidenceType.BEFORE_PHOTO
        ),
        file_name="before.jpg",
        registered_by_person_code="55464",
        created_at=datetime(
            2026,
            8,
            18,
            17,
            0,
        ),
        description="Estado inicial.",
        activity_code=activity_code,
    )


def build_use_case(
    person_active=True,
):

    evidence_repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    work_order_repository = (
        InMemoryWorkOrderRepository()
    )

    person_repository = (
        FakePersonRepository()
    )

    activity_repository = (
        InMemoryWorkOrderActivityRepository()
    )

    work_order_repository.save(
        create_work_order()
    )

    person_repository.save(
        SimpleNamespace(
            code="55464",
            is_active=person_active,
        )
    )

    activity_repository.save(
        WorkOrderActivity(
            code="ACT-001",
            work_order_code="WO-001",
            title="Inspección",
            responsible_person_code="55464",
        )
    )

    use_case = CreateWorkOrderEvidence(
        evidence_repository,
        work_order_repository,
        person_repository,
        activity_repository,
    )

    return (
        evidence_repository,
        work_order_repository,
        person_repository,
        activity_repository,
        use_case,
    )


def test_should_create_work_order_evidence():

    (
        evidence_repository,
        _,
        _,
        _,
        use_case,
    ) = build_use_case()

    result = use_case.execute(
        create_command()
    )

    assert (
        result.evidence.evidence_id
        == "EVID-001"
    )

    assert (
        result.evidence.work_order_code
        == "WO-001"
    )

    assert (
        result.evidence.activity_code
        == "ACT-001"
    )

    persisted = (
        evidence_repository.get_by_id(
            "EVID-001"
        )
    )

    assert persisted is not None


def test_should_allow_evidence_without_activity():

    (
        _,
        _,
        _,
        _,
        use_case,
    ) = build_use_case()

    result = use_case.execute(
        create_command(
            activity_code=None
        )
    )

    assert (
        result.evidence.activity_code
        is None
    )


def test_should_reject_duplicate_evidence():

    (
        evidence_repository,
        _,
        _,
        _,
        use_case,
    ) = build_use_case()

    first = use_case.execute(
        create_command()
    )

    assert first.evidence is not None

    with pytest.raises(
        ValueError,
        match="evidence already exists",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_work_order():

    (
        _,
        work_order_repository,
        _,
        _,
        use_case,
    ) = build_use_case()

    work_order_repository.delete(
        "WO-001"
    )

    with pytest.raises(
        ValueError,
        match="work order not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_person():

    (
        _,
        _,
        person_repository,
        _,
        use_case,
    ) = build_use_case()

    person_repository._people.clear()

    with pytest.raises(
        ValueError,
        match="registered person not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_inactive_person():

    (
        _,
        _,
        _,
        _,
        use_case,
    ) = build_use_case(
        person_active=False
    )

    with pytest.raises(
        ValueError,
        match="registered person is inactive",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_unknown_activity():

    (
        _,
        _,
        _,
        activity_repository,
        use_case,
    ) = build_use_case()

    activity_repository.delete(
        "ACT-001"
    )

    with pytest.raises(
        ValueError,
        match="activity not found",
    ):
        use_case.execute(
            create_command()
        )


def test_should_reject_activity_from_other_work_order():

    (
        _,
        _,
        _,
        activity_repository,
        use_case,
    ) = build_use_case()

    activity_repository.delete(
        "ACT-001"
    )

    activity_repository.save(
        WorkOrderActivity(
            code="ACT-001",
            work_order_code="WO-OTHER",
            title="Otra actividad",
            responsible_person_code="55464",
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "activity does not belong "
            "to work order"
        ),
    ):
        use_case.execute(
            create_command()
        )
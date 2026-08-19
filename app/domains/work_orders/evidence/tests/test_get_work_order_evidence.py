from datetime import datetime

import pytest

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.repositories import (
    InMemoryWorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.use_cases import (
    GetWorkOrderEvidence,
    GetWorkOrderEvidenceQuery,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)


def test_should_get_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        WorkOrderEvidence(
            evidence_id="EVID-001",
            work_order_code="WO-001",
            title="Foto",
            evidence_type=EvidenceType.BEFORE_PHOTO,
            file_name="EVID-001.jpg",
            registered_by_person_code="55464",
            created_at=datetime(
                2026,
                8,
                18,
            ),
        )
    )

    use_case = GetWorkOrderEvidence(
        repository
    )

    result = use_case.execute(
        GetWorkOrderEvidenceQuery(
            evidence_id=" evid-001 "
        )
    )

    assert (
        result.evidence.evidence_id
        == "EVID-001"
    )


def test_should_reject_missing_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    use_case = GetWorkOrderEvidence(
        repository
    )

    with pytest.raises(
        ValueError,
        match="evidence not found",
    ):
        use_case.execute(
            GetWorkOrderEvidenceQuery(
                evidence_id="EVID-X"
            )
        )
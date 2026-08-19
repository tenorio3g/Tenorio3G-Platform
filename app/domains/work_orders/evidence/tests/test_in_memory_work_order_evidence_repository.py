from datetime import datetime

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.repositories import (
    InMemoryWorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)


def create_evidence(
    evidence_id="EVID-001",
    work_order_code="WO-001",
):

    return WorkOrderEvidence(
        evidence_id=evidence_id,
        work_order_code=work_order_code,
        title="Foto de prueba",
        evidence_type=EvidenceType.BEFORE_PHOTO,
        file_name="evidence.jpg",
        registered_by_person_code="55464",
        created_at=datetime(
            2026,
            8,
            18,
            17,
            0,
        ),
    )


def test_should_save_and_get_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        create_evidence()
    )

    result = repository.get_by_id(
        "EVID-001"
    )

    assert result is not None
    assert result.evidence_id == "EVID-001"


def test_should_normalize_evidence_id():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        create_evidence()
    )

    result = repository.get_by_id(
        " evid-001 "
    )

    assert result is not None


def test_should_list_by_work_order():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        create_evidence(
            evidence_id="EVID-001",
            work_order_code="WO-001",
        )
    )

    repository.save(
        create_evidence(
            evidence_id="EVID-002",
            work_order_code="WO-002",
        )
    )

    result = repository.list_by_work_order(
        " wo-001 "
    )

    assert len(result) == 1
    assert result[0].evidence_id == "EVID-001"


def test_should_delete_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        create_evidence()
    )

    repository.delete(
        " evid-001 "
    )

    assert (
        repository.get_by_id(
            "EVID-001"
        )
        is None
    )
from datetime import datetime

import pytest

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)


def create_evidence():

    return WorkOrderEvidence(
        evidence_id="EVID-001",
        work_order_code="WO-001",
        title="Contactor dañado",
        evidence_type=EvidenceType.BEFORE_PHOTO,
        file_name="evid_001.jpg",
        registered_by_person_code="55464",
        created_at=datetime(
            2026,
            8,
            18,
            16,
            45,
        ),
        description="Estado antes del reemplazo.",
        activity_code="ACT-001",
    )


def test_should_create_work_order_evidence():

    evidence = create_evidence()

    assert evidence.evidence_id == "EVID-001"
    assert evidence.work_order_code == "WO-001"
    assert evidence.title == "Contactor dañado"

    assert (
        evidence.evidence_type
        == EvidenceType.BEFORE_PHOTO
    )

    assert evidence.file_name == "evid_001.jpg"

    assert (
        evidence.registered_by_person_code
        == "55464"
    )

    assert evidence.activity_code == "ACT-001"


@pytest.mark.parametrize(
    "field_name",
    [
        "evidence_id",
        "work_order_code",
        "title",
        "file_name",
        "registered_by_person_code",
    ],
)
def test_should_require_fields(
    field_name,
):

    data = {
        "evidence_id": "EVID-001",
        "work_order_code": "WO-001",
        "title": "Contactor dañado",
        "evidence_type": EvidenceType.BEFORE_PHOTO,
        "file_name": "evid_001.jpg",
        "registered_by_person_code": "55464",
        "created_at": datetime(
            2026,
            8,
            18,
        ),
    }

    data[field_name] = ""

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        WorkOrderEvidence(
            **data
        )


def test_should_require_valid_evidence_type():

    with pytest.raises(
        ValueError,
        match="evidence_type must be an EvidenceType",
    ):
        WorkOrderEvidence(
            evidence_id="EVID-001",
            work_order_code="WO-001",
            title="Prueba",
            evidence_type="BEFORE_PHOTO",
            file_name="x.jpg",
            registered_by_person_code="55464",
            created_at=datetime(
                2026,
                8,
                18,
            ),
        )


def test_should_require_created_at_datetime():

    with pytest.raises(
        ValueError,
        match="created_at must be a datetime",
    ):
        WorkOrderEvidence(
            evidence_id="EVID-001",
            work_order_code="WO-001",
            title="Prueba",
            evidence_type=EvidenceType.OTHER,
            file_name="x.jpg",
            registered_by_person_code="55464",
            created_at="2026-08-18",
        )


def test_should_allow_evidence_without_activity():

    evidence = WorkOrderEvidence(
        evidence_id="EVID-002",
        work_order_code="WO-001",
        title="Medición final",
        evidence_type=EvidenceType.MEASUREMENT,
        file_name="medicion.pdf",
        registered_by_person_code="55464",
        created_at=datetime(
            2026,
            8,
            18,
        ),
    )

    assert evidence.activity_code is None


def test_should_normalize_codes():

    evidence = WorkOrderEvidence(
        evidence_id=" evid-003 ",
        work_order_code=" wo-001 ",
        title="Foto final",
        evidence_type=EvidenceType.AFTER_PHOTO,
        file_name="final.jpg",
        registered_by_person_code="55464",
        created_at=datetime(
            2026,
            8,
            18,
        ),
        activity_code=" act-001 ",
    )

    assert evidence.evidence_id == "EVID-003"
    assert evidence.work_order_code == "WO-001"
    assert evidence.activity_code == "ACT-001"
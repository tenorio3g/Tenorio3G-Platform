from datetime import datetime

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.presentation import (
    WorkOrderEvidencePresenter,
)

from app.domains.work_orders.evidence.repositories import (
    InMemoryWorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.use_cases import (
    ListWorkOrderEvidence,
    ListWorkOrderEvidenceQuery,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)


def create_evidence(
    evidence_id="EVID-001",
    evidence_type=EvidenceType.BEFORE_PHOTO,
):

    return WorkOrderEvidence(
        evidence_id=evidence_id,
        work_order_code="WO-001",
        title="Contactor dañado",
        evidence_type=evidence_type,
        file_name="evidence.jpg",
        registered_by_person_code="55464",
        created_at=datetime(
            2026,
            8,
            18,
            17,
            30,
        ),
        description="Evidencia técnica.",
        activity_code="ACT-001",
    )


def test_should_list_and_present_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        create_evidence()
    )

    use_case = ListWorkOrderEvidence(
        repository
    )

    result = use_case.execute(
        ListWorkOrderEvidenceQuery(
            work_order_code=" wo-001 "
        )
    )

    view_model = (
        WorkOrderEvidencePresenter.present(
            result
        )
    )

    assert view_model.has_items is True
    assert view_model.total == 1

    item = view_model.items[0]

    assert item.evidence_id == "EVID-001"
    assert item.title == "Contactor dañado"

    assert (
        item.evidence_type
        == "BEFORE_PHOTO"
    )

    assert (
        item.evidence_type_label
        == "Foto antes"
    )

    assert (
        item.created_at
        == "18/08/2026 17:30"
    )

    assert item.activity_code == "ACT-001"


def test_should_present_other_evidence_types():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        create_evidence(
            evidence_id="EVID-001",
            evidence_type=(
                EvidenceType.AFTER_PHOTO
            ),
        )
    )

    repository.save(
        create_evidence(
            evidence_id="EVID-002",
            evidence_type=(
                EvidenceType.MEASUREMENT
            ),
        )
    )

    repository.save(
        create_evidence(
            evidence_id="EVID-003",
            evidence_type=(
                EvidenceType.DOCUMENT
            ),
        )
    )

    use_case = ListWorkOrderEvidence(
        repository
    )

    result = use_case.execute(
        ListWorkOrderEvidenceQuery(
            work_order_code="WO-001"
        )
    )

    view_model = (
        WorkOrderEvidencePresenter.present(
            result
        )
    )

    labels = [
        item.evidence_type_label
        for item in view_model.items
    ]

    assert "Foto después" in labels
    assert "Medición" in labels
    assert "Documento" in labels


def test_should_present_empty_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    use_case = ListWorkOrderEvidence(
        repository
    )

    result = use_case.execute(
        ListWorkOrderEvidenceQuery(
            work_order_code="WO-001"
        )
    )

    view_model = (
        WorkOrderEvidencePresenter.present(
            result
        )
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    

def test_should_detect_pdf_evidence():

    repository = (
        InMemoryWorkOrderEvidenceRepository()
    )

    repository.save(
        WorkOrderEvidence(
            evidence_id="EVID-PDF",
            work_order_code="WO-001",
            title="Reporte técnico",
            evidence_type=EvidenceType.DOCUMENT,
            file_name="reporte.pdf",
            registered_by_person_code="55464",
            created_at=datetime(
                2026,
                8,
                18,
            ),
        )
    )

    use_case = ListWorkOrderEvidence(
        repository
    )

    result = use_case.execute(
        ListWorkOrderEvidenceQuery(
            work_order_code="WO-001"
        )
    )

    view_model = (
        WorkOrderEvidencePresenter.present(
            result
        )
    )

    item = view_model.items[0]

    assert item.is_image is False
    assert item.is_pdf is True
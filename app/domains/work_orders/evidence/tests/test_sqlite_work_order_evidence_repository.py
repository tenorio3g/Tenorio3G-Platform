from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.foundation.database import Base

from app.domains.work_orders.evidence.entities import (
    WorkOrderEvidence,
)

from app.domains.work_orders.evidence.repositories import (
    SQLiteWorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)


def create_repository():

    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(
        engine
    )

    session_factory = sessionmaker(
        bind=engine
    )

    return SQLiteWorkOrderEvidenceRepository(
        session_factory
    )


def create_evidence(
    evidence_id="EVID-001",
    work_order_code="WO-001",
):

    return WorkOrderEvidence(
        evidence_id=evidence_id,
        work_order_code=work_order_code,
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


def test_should_save_and_get_evidence():

    repository = create_repository()

    repository.save(
        create_evidence()
    )

    result = repository.get_by_id(
        "EVID-001"
    )

    assert result is not None
    assert result.evidence_id == "EVID-001"
    assert result.work_order_code == "WO-001"
    assert result.title == "Contactor dañado"

    assert (
        result.evidence_type
        == EvidenceType.BEFORE_PHOTO
    )

    assert result.file_name == "evid_001.jpg"

    assert (
        result.registered_by_person_code
        == "55464"
    )

    assert result.activity_code == "ACT-001"


def test_should_list_by_work_order():

    repository = create_repository()

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


def test_should_update_existing_evidence():

    repository = create_repository()

    evidence = create_evidence()

    repository.save(
        evidence
    )

    evidence.title = "Contactor reemplazado"
    evidence.description = "Trabajo terminado."

    repository.save(
        evidence
    )

    result = repository.get_by_id(
        "EVID-001"
    )

    assert result is not None

    assert (
        result.title
        == "Contactor reemplazado"
    )

    assert (
        result.description
        == "Trabajo terminado."
    )


def test_should_delete_evidence():

    repository = create_repository()

    repository.save(
        create_evidence()
    )

    repository.delete(
        " evid-001 "
    )

    result = repository.get_by_id(
        "EVID-001"
    )

    assert result is None


def test_should_return_none_when_not_found():

    repository = create_repository()

    result = repository.get_by_id(
        "EVID-NOT-FOUND"
    )

    assert result is None
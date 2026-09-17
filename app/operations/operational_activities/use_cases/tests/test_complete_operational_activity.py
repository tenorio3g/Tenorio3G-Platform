from datetime import datetime

import pytest

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
    OperationalActivityStatus,
)
from app.operations.operational_activities.repositories.in_memory_operational_activity_repository import (
    InMemoryOperationalActivityRepository,
)
from app.operations.operational_activities.use_cases.complete_operational_activity import (
    CompleteOperationalActivity,
)


def test_should_complete_open_operational_activity():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-014",
        description="Revisi?n de alumbrado exterior",
        started_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        area="Exterior",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    ended_at = datetime(
        2026,
        9,
        17,
        9,
        30,
    )

    completed_activity = use_case.execute(
        code="OP-ACT-014",
        completed_by_person_code="TECH-001",
        completed_at=ended_at,
        ended_at=ended_at,
        result_notes=(
            "Alumbrado revisado sin anomal?as"
        ),
    )

    saved_activity = repository.get_by_code(
        "OP-ACT-014"
    )

    assert completed_activity is activity
    assert saved_activity is activity

    assert activity.ended_at == ended_at
    assert activity.result_notes == (
        "Alumbrado revisado sin anomal?as"
    )

    assert activity.status == (
        OperationalActivityStatus.COMPLETED
    )

def test_should_reject_completion_when_activity_does_not_exist():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="^operational activity not found$",
    ):
        use_case.execute(
            code="OP-ACT-999",
            ended_at=datetime(
                2026,
                9,
                17,
                10,
                0,
            ),
            result_notes="Actividad terminada",
        )

    assert repository.get_by_code(
        "OP-ACT-999"
    ) is None

def test_should_reject_completion_when_activity_is_already_completed():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    original_ended_at = datetime(
        2026,
        9,
        17,
        9,
        30,
    )

    activity = OperationalActivity(
        code="OP-ACT-015",
        description="Revisi?n de tablero",
        started_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        ended_at=original_ended_at,
        result_notes="Revisi?n terminada correctamente",
        area="MD2",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="^activity is already completed$",
    ):
        use_case.execute(
            code="OP-ACT-015",
            completed_by_person_code="TECH-001",
            completed_at=datetime(
                2026,
                9,
                17,
                10,
                0,
            ),
            ended_at=datetime(
                2026,
                9,
                17,
                10,
                0,
            ),
            result_notes=(
                "Este resultado no debe guardarse"
            ),
        )

    saved_activity = repository.get_by_code(
        "OP-ACT-015"
    )

    assert saved_activity is activity

    assert activity.ended_at == (
        original_ended_at
    )

    assert activity.result_notes == (
        "Revisi?n terminada correctamente"
    )

    assert activity.status == (
        OperationalActivityStatus.COMPLETED
    )

def test_should_reject_completion_when_ended_at_is_before_started_at():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-016",
        description="Revisi?n de compresor",
        started_at=datetime(
            2026,
            9,
            17,
            10,
            0,
        ),
        area="Compresores",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match=(
            "^ended_at cannot be before started_at$"
        ),
    ):
        use_case.execute(
            code="OP-ACT-016",
            completed_by_person_code="TECH-001",
            completed_at=datetime(
                2026,
                9,
                17,
                10,
                0,
            ),
            ended_at=datetime(
                2026,
                9,
                17,
                9,
                59,
            ),
            result_notes=(
                "Este resultado no debe guardarse"
            ),
        )

    saved_activity = repository.get_by_code(
        "OP-ACT-016"
    )

    assert saved_activity is activity

    assert activity.ended_at is None
    assert activity.result_notes == ""

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

def test_should_normalize_code_when_completing_activity():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-017",
        description="Revisi?n de manejadora",
        started_at=datetime(
            2026,
            9,
            17,
            11,
            0,
        ),
        area="Planta alta",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    completed_activity = use_case.execute(
        code="   op-act-017   ",
        completed_by_person_code="TECH-001",
        completed_at=datetime(
            2026,
            9,
            17,
            12,
            30,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            12,
            30,
        ),
        result_notes=(
            "Manejadora revisada correctamente"
        ),
    )

    assert completed_activity is activity

    assert activity.status == (
        OperationalActivityStatus.COMPLETED
    )

    assert activity.ended_at == datetime(
        2026,
        9,
        17,
        12,
        30,
    )

    assert activity.result_notes == (
        "Manejadora revisada correctamente"
    )

@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_blank_code_when_completing(
    code,
):
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="^code is required$",
    ):
        use_case.execute(
            code=code,
            ended_at=datetime(
                2026,
                9,
                17,
                13,
                0,
            ),
            result_notes="Actividad terminada",
        )

    assert repository.list_all() == []

def test_should_normalize_result_notes_when_completing():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-018",
        description="Revisi?n de alumbrado",
        started_at=datetime(
            2026,
            9,
            17,
            13,
            0,
        ),
        area="Recibos",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    completed_activity = use_case.execute(
        code="OP-ACT-018",
        completed_by_person_code="TECH-001",
        completed_at=datetime(
            2026,
            9,
            17,
            14,
            0,
        ),
        ended_at=datetime(
            2026,
            9,
            17,
            14,
            0,
        ),
        result_notes=(
            "   Sin anomal?as detectadas   "
        ),
    )

    assert completed_activity is activity

    assert activity.result_notes == (
        "Sin anomal?as detectadas"
    )

def test_should_record_completion_audit_data():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-019",
        description=(
            "Revisi?n de alimentaci?n "
            "de c?maras"
        ),
        started_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        area="Sistemas",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    ended_at = datetime(
        2026,
        9,
        17,
        9,
        0,
    )

    completed_at = datetime(
        2026,
        9,
        17,
        9,
        12,
    )

    completed_activity = use_case.execute(
        code="OP-ACT-019",
        ended_at=ended_at,
        result_notes=(
            "Alimentaci?n revisada "
            "correctamente"
        ),
        completed_at=completed_at,
        completed_by_person_code="TECH-001",
    )

    assert completed_activity is activity

    assert activity.ended_at == ended_at

    assert activity.completed_at == (
        completed_at
    )

    assert (
        activity.completed_by_person_code
        == "TECH-001"
    )

    assert activity.status == (
        OperationalActivityStatus.COMPLETED
    )

def test_should_normalize_completed_by_person_code():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-021",
        description="Revisi?n de tablero el?ctrico",
        started_at=datetime(
            2026,
            9,
            17,
            14,
            0,
        ),
        area="Producci?n",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    completed_at = datetime(
        2026,
        9,
        17,
        15,
        10,
    )

    completed_activity = use_case.execute(
        code="OP-ACT-021",
        ended_at=datetime(
            2026,
            9,
            17,
            15,
            0,
        ),
        result_notes="Revisi?n terminada",
        completed_at=completed_at,
        completed_by_person_code=(
            "   tech-001   "
        ),
    )

    assert completed_activity is activity

    assert (
        activity.completed_by_person_code
        == "TECH-001"
    )

    assert activity.completed_at == (
        completed_at
    )

@pytest.mark.parametrize(
    "completed_by_person_code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_blank_completed_by_person_code(
    completed_by_person_code,
):
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-022",
        description="Revisi?n de equipo",
        started_at=datetime(
            2026,
            9,
            17,
            15,
            0,
        ),
        area="Producci?n",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match=(
            "^completed_by_person_code is required$"
        ),
    ):
        use_case.execute(
            code="OP-ACT-022",
            ended_at=datetime(
                2026,
                9,
                17,
                16,
                0,
            ),
            result_notes="Actividad terminada",
            completed_at=datetime(
                2026,
                9,
                17,
                16,
                5,
            ),
            completed_by_person_code=(
                completed_by_person_code
            ),
        )

    saved_activity = repository.get_by_code(
        "OP-ACT-022"
    )

    assert saved_activity is activity

    assert activity.ended_at is None
    assert activity.completed_at is None

    assert (
        activity.completed_by_person_code
        == ""
    )

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

def test_should_reject_missing_completed_at():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    activity = OperationalActivity(
        code="OP-ACT-023",
        description="Revisi?n de instalaci?n el?ctrica",
        started_at=datetime(
            2026,
            9,
            17,
            16,
            0,
        ),
        area="Producci?n",
        created_by_person_code="SUP-001",
    )

    repository.save(activity)

    use_case = CompleteOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="^completed_at is required$",
    ):
        use_case.execute(
            code="OP-ACT-023",
            ended_at=datetime(
                2026,
                9,
                17,
                16,
                30,
            ),
            result_notes="Trabajo terminado",
            completed_at=None,
            completed_by_person_code="TECH-001",
        )

    saved_activity = repository.get_by_code(
        "OP-ACT-023"
    )

    assert saved_activity is activity

    assert activity.ended_at is None
    assert activity.result_notes == ""
    assert activity.completed_at is None

    assert (
        activity.completed_by_person_code
        == ""
    )

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )


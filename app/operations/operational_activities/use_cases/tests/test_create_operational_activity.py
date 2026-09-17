from datetime import datetime

import pytest

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivitySource,
    OperationalActivityStatus,
)
from app.operations.operational_activities.repositories.in_memory_operational_activity_repository import (
    InMemoryOperationalActivityRepository,
)
from app.operations.operational_activities.use_cases.create_operational_activity import (
    CreateOperationalActivity,
)


def test_should_create_open_operational_activity_without_work_order():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    started_at = datetime(
        2026,
        9,
        17,
        7,
        0,
    )

    activity = use_case.execute(
        code="OP-ACT-007",
        description="Revisi?n de alumbrado exterior",
        started_at=started_at,
        area="Exterior",
        created_by_person_code="SUP-001",
    )

    saved_activity = repository.get_by_code(
        "OP-ACT-007"
    )

    assert saved_activity is activity

    assert activity.code == "OP-ACT-007"
    assert activity.description == (
        "Revisi?n de alumbrado exterior"
    )
    assert activity.started_at == started_at
    assert activity.ended_at is None
    assert activity.area == "Exterior"
    assert activity.work_order_code is None

    assert activity.source == (
        OperationalActivitySource.MANUAL
    )

    assert activity.status == (
        OperationalActivityStatus.IN_PROGRESS
    )

    assert activity.created_by_person_code == (
        "SUP-001"
    )

def test_should_reject_duplicate_operational_activity_code():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    first_activity = use_case.execute(
        code="OP-ACT-008",
        description="Primera actividad",
        started_at=datetime(
            2026,
            9,
            17,
            8,
            0,
        ),
        created_by_person_code="SUP-001",
    )

    try:
        use_case.execute(
            code="OP-ACT-008",
            description="Segunda actividad",
            started_at=datetime(
                2026,
                9,
                17,
                9,
                0,
            ),
            created_by_person_code="SUP-001",
        )
    except ValueError as exc:
        assert str(exc) == (
            "operational activity code already exists"
        )
    else:
        raise AssertionError(
            "Expected ValueError for duplicate code"
        )

    saved_activity = repository.get_by_code(
        "OP-ACT-008"
    )

    assert saved_activity is first_activity
    assert saved_activity.description == (
        "Primera actividad"
    )

@pytest.mark.parametrize(
    "description",
    [
        "",
        "   ",
    ],
)
def test_should_reject_blank_description(
    description,
):
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="^description is required$",
    ):
        use_case.execute(
            code="OP-ACT-009",
            description=description,
            started_at=datetime(
                2026,
                9,
                17,
                10,
                0,
            ),
            created_by_person_code="SUP-001",
        )

    assert repository.get_by_code(
        "OP-ACT-009"
    ) is None

def test_should_normalize_description():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    activity = use_case.execute(
        code="OP-ACT-010",
        description=(
            "   Revisi?n de alumbrado exterior   "
        ),
        started_at=datetime(
            2026,
            9,
            17,
            11,
            0,
        ),
        created_by_person_code="SUP-001",
    )

    assert activity.description == (
        "Revisi?n de alumbrado exterior"
    )

    saved_activity = repository.get_by_code(
        "OP-ACT-010"
    )

    assert saved_activity is activity
    assert saved_activity.description == (
        "Revisi?n de alumbrado exterior"
    )

@pytest.mark.parametrize(
    "code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_blank_code(
    code,
):
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match="^code is required$",
    ):
        use_case.execute(
            code=code,
            description="Revisi?n de alumbrado",
            started_at=datetime(
                2026,
                9,
                17,
                12,
                0,
            ),
            created_by_person_code="SUP-001",
        )

    assert repository.list_all() == []

def test_should_reject_duplicate_code_after_normalization():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    first_activity = use_case.execute(
        code="OP-ACT-011",
        description="Primera actividad",
        started_at=datetime(
            2026,
            9,
            17,
            13,
            0,
        ),
        created_by_person_code="SUP-001",
    )

    with pytest.raises(
        ValueError,
        match=(
            "^operational activity code "
            "already exists$"
        ),
    ):
        use_case.execute(
            code="   op-act-011   ",
            description="Segunda actividad",
            started_at=datetime(
                2026,
                9,
                17,
                14,
                0,
            ),
            created_by_person_code="SUP-001",
        )

    activities = repository.list_all()

    assert activities == [
        first_activity,
    ]

    assert repository.get_by_code(
        "OP-ACT-011"
    ) is first_activity

    assert first_activity.description == (
        "Primera actividad"
    )

@pytest.mark.parametrize(
    "created_by_person_code",
    [
        "",
        "   ",
    ],
)
def test_should_reject_blank_created_by_person_code(
    created_by_person_code,
):
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    with pytest.raises(
        ValueError,
        match=(
            "^created_by_person_code is required$"
        ),
    ):
        use_case.execute(
            code="OP-ACT-012",
            description="Revisi?n de alumbrado",
            started_at=datetime(
                2026,
                9,
                17,
                15,
                0,
            ),
            created_by_person_code=(
                created_by_person_code
            ),
        )

    assert repository.get_by_code(
        "OP-ACT-012"
    ) is None

def test_should_normalize_created_by_person_code():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    activity = use_case.execute(
        code="OP-ACT-013",
        description="Revisi?n de alumbrado",
        started_at=datetime(
            2026,
            9,
            17,
            15,
            30,
        ),
        created_by_person_code="   sup-001   ",
    )

    assert activity.created_by_person_code == (
        "SUP-001"
    )

    saved_activity = repository.get_by_code(
        "OP-ACT-013"
    )

    assert saved_activity is activity
    assert saved_activity.created_by_person_code == (
        "SUP-001"
    )


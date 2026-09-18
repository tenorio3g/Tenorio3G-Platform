from datetime import datetime
from importlib import import_module

import pytest

from app.operations.operational_activities.entities.operational_activity import (
    OperationalActivity,
    OperationalActivitySource,
    OperationalActivityStatus,
)
from app.operations.operational_activities.repositories.in_memory_operational_activity_repository import (
    InMemoryOperationalActivityRepository,
)
from app.operations.operational_activities.use_cases.create_operational_activity import (
    CreateOperationalActivity,
)


def create_use_case():
    repository = (
        InMemoryOperationalActivityRepository()
    )

    use_case = CreateOperationalActivity(
        repository=repository,
    )

    return repository, use_case


def test_should_create_open_operational_activity_without_work_order():
    repository, use_case = create_use_case()

    started_at = datetime(
        2026,
        9,
        17,
        7,
        0,
    )

    activity = use_case.execute(
        description="Revision de alumbrado exterior",
        started_at=started_at,
        area="Exterior",
        created_by_person_code="SUP-001",
    )

    saved_activity = repository.get_by_code(
        activity.code
    )

    assert saved_activity is activity

    assert activity.code.startswith(
        "OPA-"
    )

    assert activity.description == (
        "Revision de alumbrado exterior"
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
    repository, use_case = create_use_case()

    with pytest.raises(
        ValueError,
        match="^description is required$",
    ):
        use_case.execute(
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

    assert repository.list_all() == []


def test_should_normalize_description():
    repository, use_case = create_use_case()

    activity = use_case.execute(
        description=(
            "   Revision de alumbrado exterior   "
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
        "Revision de alumbrado exterior"
    )

    saved_activity = repository.get_by_code(
        activity.code
    )

    assert saved_activity is activity

    assert saved_activity.description == (
        "Revision de alumbrado exterior"
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
    repository, use_case = create_use_case()

    with pytest.raises(
        ValueError,
        match=(
            "^created_by_person_code is required$"
        ),
    ):
        use_case.execute(
            description="Revision de alumbrado",
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

    assert repository.list_all() == []


def test_should_normalize_created_by_person_code():
    repository, use_case = create_use_case()

    activity = use_case.execute(
        description="Revision de alumbrado",
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
        activity.code
    )

    assert saved_activity is activity

    assert saved_activity.created_by_person_code == (
        "SUP-001"
    )


def test_should_retry_when_generated_code_already_exists(
    monkeypatch,
):
    repository, use_case = create_use_case()

    existing_activity = OperationalActivity(
        code="OPA-AAAAAAAA",
        description="Actividad existente",
        started_at=datetime(
            2026,
            9,
            17,
            6,
            0,
        ),
        source=OperationalActivitySource.MANUAL,
        created_by_person_code="SUP-001",
    )

    repository.save(
        existing_activity
    )

    class FakeUUID:
        def __init__(
            self,
            hex_value,
        ):
            self.hex = hex_value

    generated_values = iter(
        [
            FakeUUID(
                "aaaaaaaa111111111111111111111111"
            ),
            FakeUUID(
                "bbbbbbbb222222222222222222222222"
            ),
        ]
    )

    module = import_module(
        "app.operations.operational_activities"
        ".use_cases.create_operational_activity"
    )

    monkeypatch.setattr(
        module,
        "uuid4",
        lambda: next(
            generated_values
        ),
    )

    activity = use_case.execute(
        description="Nueva actividad",
        started_at=datetime(
            2026,
            9,
            17,
            7,
            0,
        ),
        created_by_person_code="SUP-001",
    )

    assert activity.code == (
        "OPA-BBBBBBBB"
    )

    assert (
        repository.get_by_code(
            "OPA-AAAAAAAA"
        )
        is existing_activity
    )

    assert (
        repository.get_by_code(
            "OPA-BBBBBBBB"
        )
        is activity
    )

    assert len(
        repository.list_all()
    ) == 2

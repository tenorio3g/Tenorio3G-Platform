from datetime import datetime

import pytest

from app.domains.work_orders.work_sessions.entities import (
    WorkSession,
)

from app.domains.work_orders.work_sessions.value_objects import (
    WorkSessionSource,
)


def create_work_session(
    *,
    code: str = "WS-001",
    work_order_code: str = "WO-001",
    activity_code: str = "ACT-001",
    person_code: str = "TECH-001",
    started_at: datetime | None = None,
    ended_at: datetime | None = None,
    source: WorkSessionSource = WorkSessionSource.AUTOMATIC,
    created_at: datetime | None = None,
    created_by_person_code: str = "TECH-001",
) -> WorkSession:

    return WorkSession(
        code=code,
        work_order_code=work_order_code,
        activity_code=activity_code,
        person_code=person_code,
        started_at=started_at
        or datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
        ended_at=ended_at,
        source=source,
        created_at=created_at
        or datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
        created_by_person_code=(
            created_by_person_code
        ),
    )


def test_should_create_automatic_work_session():

    session = create_work_session()

    assert session.code == "WS-001"

    assert session.work_order_code == "WO-001"

    assert session.activity_code == "ACT-001"

    assert session.person_code == "TECH-001"

    assert (
        session.source
        == WorkSessionSource.AUTOMATIC
    )

    assert session.is_active is True

    assert session.ended_at is None

    assert session.duration_minutes is None


def test_should_create_manual_work_session():

    session = create_work_session(
        code="WS-MANUAL-001",
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    assert (
        session.source
        == WorkSessionSource.MANUAL
    )

    assert session.is_active is False

    assert session.duration_minutes == 60


def test_should_end_active_work_session():

    session = create_work_session()

    session.end(
        datetime(
            2026,
            8,
            26,
            8,
            30,
        )
    )

    assert session.is_active is False

    assert session.ended_at == datetime(
        2026,
        8,
        26,
        8,
        30,
    )

    assert session.duration_minutes == 90


def test_should_reject_end_before_start():

    session = create_work_session()

    with pytest.raises(
        ValueError,
        match="end cannot be before start",
    ):
        session.end(
            datetime(
                2026,
                8,
                26,
                6,
                59,
            )
        )


def test_should_reject_ending_session_twice():

    session = create_work_session()

    session.end(
        datetime(
            2026,
            8,
            26,
            8,
            0,
        )
    )

    with pytest.raises(
        ValueError,
        match="work session already ended",
    ):
        session.end(
            datetime(
                2026,
                8,
                26,
                9,
                0,
            )
        )


def test_should_reject_ended_at_before_started_at():

    with pytest.raises(
        ValueError,
        match="end cannot be before start",
    ):
        create_work_session(
            started_at=datetime(
                2026,
                8,
                26,
                8,
                0,
            ),
            ended_at=datetime(
                2026,
                8,
                26,
                7,
                59,
            ),
        )


def test_should_normalize_codes():

    session = create_work_session(
        code="  ws-001  ",
        work_order_code="  wo-001  ",
        activity_code="  act-001  ",
        person_code="  tech-001  ",
        created_by_person_code=(
            "  supervisor-001  "
        ),
    )

    assert session.code == "WS-001"

    assert session.work_order_code == "WO-001"

    assert session.activity_code == "ACT-001"

    assert session.person_code == "TECH-001"

    assert (
        session.created_by_person_code
        == "SUPERVISOR-001"
    )
def test_should_reject_empty_code():

    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        create_work_session(
            code="   ",
        )


def test_should_reject_empty_work_order_code():

    with pytest.raises(
        ValueError,
        match="work_order_code is required",
    ):
        create_work_session(
            work_order_code="   ",
        )


def test_should_reject_empty_activity_code():

    with pytest.raises(
        ValueError,
        match="activity_code is required",
    ):
        create_work_session(
            activity_code="   ",
        )


def test_should_reject_empty_person_code():

    with pytest.raises(
        ValueError,
        match="person_code is required",
    ):
        create_work_session(
            person_code="   ",
        )


def test_should_reject_empty_created_by_person_code():

    with pytest.raises(
        ValueError,
        match="created_by_person_code is required",
    ):
        create_work_session(
            created_by_person_code="   ",
        )


def test_should_reject_invalid_started_at():

    with pytest.raises(
        ValueError,
        match="started_at must be datetime",
    ):
        create_work_session(
            started_at="2026-08-26 07:00",
        )


def test_should_reject_invalid_created_at():

    with pytest.raises(
        ValueError,
        match="created_at must be datetime",
    ):
        create_work_session(
            created_at="2026-08-26 07:00",
        )


def test_should_reject_invalid_ended_at():

    with pytest.raises(
        ValueError,
        match="ended_at must be datetime",
    ):
        create_work_session(
            ended_at="2026-08-26 08:00",
        )


def test_should_reject_invalid_source():

    with pytest.raises(
        ValueError,
        match="invalid work session source",
    ):
        create_work_session(
            source="AUTOMATIC",
        )


def test_should_allow_zero_duration_session():

    session = create_work_session(
        started_at=datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
        ended_at=datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
    )

    assert session.duration_minutes == 0
    assert session.is_active is False

def test_should_correct_manual_work_session_times():

    session = create_work_session(
        code="WS-MANUAL-001",
        source=WorkSessionSource.MANUAL,
        started_at=datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    session.correct(
        started_at=datetime(
            2026,
            8,
            26,
            7,
            30,
        ),
        ended_at=datetime(
            2026,
            8,
            26,
            9,
            0,
        ),
    )

    assert session.started_at == datetime(
        2026,
        8,
        26,
        7,
        30,
    )

    assert session.ended_at == datetime(
        2026,
        8,
        26,
        9,
        0,
    )

    assert session.duration_minutes == 90


def test_should_reject_correction_of_automatic_work_session():

    session = create_work_session(
        source=WorkSessionSource.AUTOMATIC,
    )

    with pytest.raises(
        ValueError,
        match="only manual work sessions can be corrected",
    ):
        session.correct(
            started_at=datetime(
                2026,
                8,
                26,
                7,
                30,
            ),
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                30,
            ),
        )


def test_should_reject_corrected_end_before_start():

    session = create_work_session(
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match="end cannot be before start",
    ):
        session.correct(
            started_at=datetime(
                2026,
                8,
                26,
                9,
                0,
            ),
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                59,
            ),
        )


def test_should_reject_invalid_corrected_started_at():

    session = create_work_session(
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match="started_at must be datetime",
    ):
        session.correct(
            started_at="2026-08-26 07:30",
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                30,
            ),
        )


def test_should_reject_invalid_corrected_ended_at():

    session = create_work_session(
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match="ended_at must be datetime",
    ):
        session.correct(
            started_at=datetime(
                2026,
                8,
                26,
                7,
                30,
            ),
            ended_at="2026-08-26 08:30",
        )


def test_should_correct_manual_work_session_times():

    session = create_work_session(
        code="WS-MANUAL-001",
        source=WorkSessionSource.MANUAL,
        started_at=datetime(
            2026,
            8,
            26,
            7,
            0,
        ),
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    session.correct(
        started_at=datetime(
            2026,
            8,
            26,
            7,
            30,
        ),
        ended_at=datetime(
            2026,
            8,
            26,
            9,
            0,
        ),
    )

    assert session.started_at == datetime(
        2026,
        8,
        26,
        7,
        30,
    )

    assert session.ended_at == datetime(
        2026,
        8,
        26,
        9,
        0,
    )

    assert session.duration_minutes == 90


def test_should_reject_correction_of_automatic_work_session():

    session = create_work_session(
        source=WorkSessionSource.AUTOMATIC,
    )

    with pytest.raises(
        ValueError,
        match="only manual work sessions can be corrected",
    ):
        session.correct(
            started_at=datetime(
                2026,
                8,
                26,
                7,
                30,
            ),
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                30,
            ),
        )


def test_should_reject_corrected_end_before_start():

    session = create_work_session(
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match="end cannot be before start",
    ):
        session.correct(
            started_at=datetime(
                2026,
                8,
                26,
                9,
                0,
            ),
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                59,
            ),
        )


def test_should_reject_invalid_corrected_started_at():

    session = create_work_session(
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match="started_at must be datetime",
    ):
        session.correct(
            started_at="2026-08-26 07:30",
            ended_at=datetime(
                2026,
                8,
                26,
                8,
                30,
            ),
        )


def test_should_reject_invalid_corrected_ended_at():

    session = create_work_session(
        source=WorkSessionSource.MANUAL,
        ended_at=datetime(
            2026,
            8,
            26,
            8,
            0,
        ),
    )

    with pytest.raises(
        ValueError,
        match="ended_at must be datetime",
    ):
        session.correct(
            started_at=datetime(
                2026,
                8,
                26,
                7,
                30,
            ),
            ended_at="2026-08-26 08:30",
        )

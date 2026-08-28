from app.domains.work_orders.work_sessions.audit.repositories import (
    SQLiteWorkSessionAuditRepository,
)

from app.domains.work_orders.work_sessions.bootstrap import (
    add_manual_work_session,
    correct_manual_work_session,
    end_work_session,
    start_work_session,
    work_session_audit_repository,
    work_session_repository,
)

from app.domains.work_orders.work_sessions.repositories import (
    SQLiteWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.use_cases import (
    AddManualWorkSession,
    CorrectManualWorkSession,
    EndWorkSession,
    StartWorkSession,
)


def test_should_build_work_session_repositories():

    assert isinstance(
        work_session_repository,
        SQLiteWorkSessionRepository,
    )

    assert isinstance(
        work_session_audit_repository,
        SQLiteWorkSessionAuditRepository,
    )


def test_should_build_work_session_use_cases():

    assert isinstance(
        start_work_session,
        StartWorkSession,
    )

    assert isinstance(
        end_work_session,
        EndWorkSession,
    )

    assert isinstance(
        add_manual_work_session,
        AddManualWorkSession,
    )

    assert isinstance(
        correct_manual_work_session,
        CorrectManualWorkSession,
    )

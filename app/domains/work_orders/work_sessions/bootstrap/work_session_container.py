from app.foundation.database import (
    SessionLocal,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.work_orders.bootstrap import (
    work_order_repository,
)

from app.domains.work_orders.activities.bootstrap import (
    work_order_activity_repository,
)

from app.domains.work_orders.work_sessions.repositories import (
    SQLiteWorkSessionRepository,
)

from app.domains.work_orders.work_sessions.audit.repositories import (
    SQLiteWorkSessionAuditRepository,
)

from app.domains.work_orders.work_sessions.use_cases import (
    AddManualWorkSession,
    CorrectManualWorkSession,
    EndWorkSession,
    StartWorkSession,
)


work_session_repository = (
    SQLiteWorkSessionRepository(
        SessionLocal
    )
)

work_session_audit_repository = (
    SQLiteWorkSessionAuditRepository(
        SessionLocal
    )
)


start_work_session = (
    StartWorkSession(
        work_order_repository,
        work_order_activity_repository,
        person_repository,
        work_session_repository,
    )
)

end_work_session = (
    EndWorkSession(
        work_session_repository,
        person_repository,
    )
)

add_manual_work_session = (
    AddManualWorkSession(
        work_order_repository,
        work_order_activity_repository,
        person_repository,
        work_session_repository,
        work_session_audit_repository,
    )
)

correct_manual_work_session = (
    CorrectManualWorkSession(
        work_session_repository,
        person_repository,
        work_session_audit_repository,
    )
)

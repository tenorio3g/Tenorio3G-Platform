from pathlib import Path

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

from app.domains.work_orders.evidence.repositories import (
    SQLiteWorkOrderEvidenceRepository,
)

from app.domains.work_orders.evidence.use_cases import (
    CreateWorkOrderEvidence,
    ListWorkOrderEvidence,
)
from app.domains.work_orders.evidence.storage import (
    LocalEvidenceStorage,
)
from app.domains.work_orders.evidence.use_cases import (
    CreateWorkOrderEvidence,
    GetWorkOrderEvidence,
    ListWorkOrderEvidence,
)

# ============================================================
# REPOSITORY
# ============================================================

work_order_evidence_repository = (
    SQLiteWorkOrderEvidenceRepository(
        SessionLocal
    )
)

# ============================================================
# STORAGE
# ============================================================

evidence_storage = LocalEvidenceStorage(
    Path(
        "storage/work_orders/evidence"
    )
)
# ============================================================
# USE CASES
# ============================================================

create_work_order_evidence = (
    CreateWorkOrderEvidence(
        work_order_evidence_repository,
        work_order_repository,
        person_repository,
        work_order_activity_repository,
    )
)

list_work_order_evidence = (
    ListWorkOrderEvidence(
        work_order_evidence_repository
    )
)
get_work_order_evidence = (
    GetWorkOrderEvidence(
        work_order_evidence_repository
    )
)
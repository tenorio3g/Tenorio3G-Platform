from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderViewModel:
    code: str
    title: str
    description: str
    work_type: str
    priority: str
    asset_code: str
    requester_person_code: str
    supervisor_person_code: str
    status: str
    created_at: str
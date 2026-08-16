from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderAssetViewModel:
    code: str
    name: str
    location_code: str


@dataclass(frozen=True)
class WorkOrderPersonViewModel:
    code: str
    name: str
    position: str


@dataclass(frozen=True)
class WorkOrderDetailViewModel:
    code: str
    title: str
    description: str
    work_type: str
    priority: str
    status: str
    created_at: str
    asset: WorkOrderAssetViewModel
    requester: WorkOrderPersonViewModel
    supervisor: WorkOrderPersonViewModel
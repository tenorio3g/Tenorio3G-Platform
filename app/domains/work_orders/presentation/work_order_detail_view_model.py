from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderAssetViewModel:
    code: str | None
    name: str
    location_code: str | None


@dataclass(frozen=True)
class WorkOrderPersonViewModel:
    code: str | None
    name: str
    position: str
    phone: str | None = None
    area: str | None = None


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

    location_description: str | None = None

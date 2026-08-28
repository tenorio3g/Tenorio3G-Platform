from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderSummaryItemViewModel:
    code: str
    title: str

    status: str
    status_label: str

    operational_state: str
    operational_state_label: str

    priority: str
    work_type: str

    asset_code: str
    asset_name: str

    requester_code: str
    requester_name: str

    supervisor_code: str
    supervisor_name: str

    technician_label: str
    technician_names: list[str]

    created_at: str


@dataclass(frozen=True)
class WorkOrderSummaryViewModel:
    items: list[
        WorkOrderSummaryItemViewModel
    ]

    @property
    def total(self) -> int:
        return len(
            self.items
        )

    @property
    def has_items(self) -> bool:
        return bool(
            self.items
        )

    @property
    def total_active(self) -> int:
        return sum(
            1
            for item in self.items
            if item.operational_state
            == "ACTIVE"
        )

    @property
    def total_finished(self) -> int:
        return sum(
            1
            for item in self.items
            if item.operational_state
            == "FINISHED"
        )

    @property
    def total_cancelled(self) -> int:
        return sum(
            1
            for item in self.items
            if item.operational_state
            == "CANCELLED"
        )

    def total_by_status(
        self,
        status: str,
    ) -> int:

        normalized_status = str(
            status
        ).strip().upper()

        return sum(
            1
            for item in self.items
            if item.status
            == normalized_status
        )

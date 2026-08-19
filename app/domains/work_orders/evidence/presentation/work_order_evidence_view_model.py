from dataclasses import dataclass


@dataclass(frozen=True)
class WorkOrderEvidenceItemViewModel:
    evidence_id: str
    title: str
    evidence_type: str
    evidence_type_label: str
    file_name: str
    registered_by_person_code: str
    created_at: str
    description: str
    activity_code: str | None
    is_image: bool
    is_pdf: bool


@dataclass(frozen=True)
class WorkOrderEvidenceViewModel:
    items: list[
        WorkOrderEvidenceItemViewModel
    ]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)
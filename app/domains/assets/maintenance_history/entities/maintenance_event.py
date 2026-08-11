from dataclasses import dataclass
from datetime import datetime


@dataclass
class MaintenanceEvent:
    code: str
    asset_code: str
    event_type: str
    title: str
    description: str
    performed_by: str
    started_at: datetime
    completed_at: datetime | None = None
    observations: str = ""

    def __post_init__(self) -> None:

        if not self.code.strip():
            raise ValueError(
                "Maintenance event code is required."
            )

        if not self.asset_code.strip():
            raise ValueError(
                "Asset code is required."
            )

        if not self.event_type.strip():
            raise ValueError(
                "Maintenance event type is required."
            )

        if not self.title.strip():
            raise ValueError(
                "Maintenance event title is required."
            )

        if not self.performed_by.strip():
            raise ValueError(
                "Performed by is required."
            )

        if (
            self.completed_at is not None
            and self.completed_at < self.started_at
        ):
            raise ValueError(
                "Completion time cannot be before start time."
            )

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None
from datetime import datetime
from enum import Enum


class OperationalActivityStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class OperationalActivitySource(str, Enum):
    MANUAL = "MANUAL"
    HISTORICAL_IMPORT = "HISTORICAL_IMPORT"


class OperationalActivity:

    def __init__(
        self,
        code: str,
        description: str,
        started_at: datetime,
        ended_at: datetime | None = None,
        result_notes: str = "",
        area: str = "",
        location_description: str = "",
        asset_code: str | None = None,
        work_order_code: str | None = None,
        source: OperationalActivitySource = (
            OperationalActivitySource.MANUAL
        ),
        created_at: datetime | None = None,
        created_by_person_code: str = "",
        completed_at: datetime | None = None,
        completed_by_person_code: str = "",
    ):
        self.code = code
        self.description = description

        if (
            ended_at is not None
            and ended_at < started_at
        ):
            raise ValueError(
                "ended_at cannot be before started_at"
            )

        self.started_at = started_at
        self.ended_at = ended_at

        self.result_notes = result_notes
        self.area = area
        self.location_description = (
            location_description
        )

        self.asset_code = asset_code
        self.work_order_code = work_order_code

        self.source = source

        self.created_at = (
            created_at
            if created_at is not None
            else datetime.now()
        )

        self.created_by_person_code = (
            created_by_person_code
        )

        self.completed_at = completed_at

        self.completed_by_person_code = (
            completed_by_person_code.strip().upper()
        )

    def complete(
        self,
        ended_at,
        result_notes="",
        completed_at=None,
        completed_by_person_code="",
    ):
        if (
            self.status
            == OperationalActivityStatus.COMPLETED
        ):
            raise ValueError(
                "activity is already completed"
            )

        if ended_at < self.started_at:
            raise ValueError(
                "ended_at cannot be before started_at"
            )

        if (
            completed_at is not None
            and completed_at < ended_at
        ):
            raise ValueError(
                "completed_at cannot be before ended_at"
            )

        normalized_result_notes = (
            result_notes.strip()
        )

        self.ended_at = ended_at

        self.result_notes = (
            normalized_result_notes
        )

        self.completed_at = completed_at

        self.completed_by_person_code = (
            completed_by_person_code.strip().upper()
        )

    @property
    def status(self) -> OperationalActivityStatus:
        if self.ended_at is None:
            return OperationalActivityStatus.IN_PROGRESS

        return OperationalActivityStatus.COMPLETED

    @property
    def work_date(self):
        return self.started_at.date()

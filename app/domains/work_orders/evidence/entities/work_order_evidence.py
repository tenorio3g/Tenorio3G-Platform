from datetime import datetime

from app.domains.work_orders.evidence.value_objects import (
    EvidenceType,
)


class WorkOrderEvidence:

    def __init__(
        self,
        evidence_id,
        work_order_code,
        title,
        evidence_type,
        file_name,
        registered_by_person_code,
        created_at,
        description="",
        activity_code=None,
    ):
        self.evidence_id = self._required(
            evidence_id,
            "evidence_id",
        ).upper()

        self.work_order_code = self._required(
            work_order_code,
            "work_order_code",
        ).upper()

        self.title = self._required(
            title,
            "title",
        )

        if not isinstance(
            evidence_type,
            EvidenceType,
        ):
            raise ValueError(
                "evidence_type must be an EvidenceType"
            )

        self.evidence_type = evidence_type

        self.file_name = self._required(
            file_name,
            "file_name",
        )

        self.registered_by_person_code = (
            self._required(
                registered_by_person_code,
                "registered_by_person_code",
            )
        )

        if not isinstance(
            created_at,
            datetime,
        ):
            raise ValueError(
                "created_at must be a datetime"
            )

        self.created_at = created_at

        self.description = str(
            description or ""
        ).strip()

        self.activity_code = (
            str(activity_code).strip().upper()
            if activity_code is not None
            and str(activity_code).strip()
            else None
        )

    @staticmethod
    def _required(
        value,
        field_name,
    ) -> str:

        normalized = str(
            value
        ).strip()

        if not normalized:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized
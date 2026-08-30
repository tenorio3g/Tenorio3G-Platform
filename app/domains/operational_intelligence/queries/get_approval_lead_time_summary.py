from dataclasses import dataclass
from datetime import timedelta

from .get_approval_lead_time import (
    ApprovalLeadTimeItem,
)


@dataclass(frozen=True)
class ApprovalLeadTimeSummary:
    total_approved: int
    average_lead_time: timedelta | None
    minimum_lead_time: timedelta | None
    maximum_lead_time: timedelta | None


class GetApprovalLeadTimeSummary:

    def execute(
        self,
        items: list[ApprovalLeadTimeItem],
    ) -> ApprovalLeadTimeSummary:

        total_approved = len(items)

        if total_approved == 0:
            return ApprovalLeadTimeSummary(
                total_approved=0,
                average_lead_time=None,
                minimum_lead_time=None,
                maximum_lead_time=None,
            )

        lead_times = [
            item.lead_time
            for item in items
        ]

        total_lead_time = sum(
            lead_times,
            timedelta(),
        )

        return ApprovalLeadTimeSummary(
            total_approved=total_approved,
            average_lead_time=(
                total_lead_time
                / total_approved
            ),
            minimum_lead_time=min(
                lead_times
            ),
            maximum_lead_time=max(
                lead_times
            ),
        )

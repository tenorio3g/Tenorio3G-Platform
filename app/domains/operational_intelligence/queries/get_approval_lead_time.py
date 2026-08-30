from dataclasses import dataclass
from datetime import datetime, timedelta

from app.foundation.timeline.engine.use_cases import (
    ListTimelineEventsQuery,
)


@dataclass(frozen=True)
class ApprovalLeadTimeItem:
    work_order_code: str
    created_at: datetime
    approved_at: datetime
    lead_time: timedelta


class GetApprovalLeadTime:

    APPROVAL_EVENT_TYPE = "WORK_ORDER_APPROVED"

    def __init__(
        self,
        work_order_repository,
        list_timeline_events,
    ):
        self._work_order_repository = (
            work_order_repository
        )
        self._list_timeline_events = (
            list_timeline_events
        )

    def execute(
        self,
    ) -> list[ApprovalLeadTimeItem]:

        result = []

        for work_order in (
            self._work_order_repository.list_all()
        ):
            approved_at = (
                self._get_approved_at(
                    work_order.code
                )
            )

            if approved_at is None:
                continue

            result.append(
                ApprovalLeadTimeItem(
                    work_order_code=
                        work_order.code,
                    created_at=
                        work_order.created_at,
                    approved_at=
                        approved_at,
                    lead_time=(
                        approved_at
                        - work_order.created_at
                    ),
                )
            )

        return result

    def _get_approved_at(
        self,
        work_order_code: str,
    ) -> datetime | None:

        timeline_result = (
            self._list_timeline_events.execute(
                ListTimelineEventsQuery(
                    entity_type="WORK_ORDER",
                    entity_code=work_order_code,
                )
            )
        )

        for event in timeline_result.items:
            if (
                event.event_type
                == self.APPROVAL_EVENT_TYPE
            ):
                return event.occurred_at

        return None

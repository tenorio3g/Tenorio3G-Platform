from app.domains.work_orders.activities.holds.value_objects import (
    ActivityHoldReason,
)

from app.domains.work_orders.activities.use_cases import (
    ListWorkOrderActivitiesResult,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from .work_order_activities_view_model import (
    ActivityHoldHistoryItemViewModel,
    WorkOrderActivitiesViewModel,
    WorkOrderActivityItemViewModel,
)


class WorkOrderActivitiesPresenter:

    STATUS_LABELS = {
        ActivityStatus.PENDING: "Pendiente",
        ActivityStatus.IN_PROGRESS: "En proceso",
        ActivityStatus.ON_HOLD: "En espera",
        ActivityStatus.COMPLETED: "Finalizada",
    }

    HOLD_REASON_LABELS = {
        ActivityHoldReason.PENDING_MATERIAL: (
            "Material pendiente"
        ),
        ActivityHoldReason.PENDING_SPARE_PART: (
            "Refacción pendiente"
        ),
        ActivityHoldReason.PENDING_PROVIDER: (
            "Proveedor pendiente"
        ),
        ActivityHoldReason.PENDING_AUTHORIZATION: (
            "Autorización pendiente"
        ),
        ActivityHoldReason.EQUIPMENT_IN_USE: (
            "Equipo en uso"
        ),
        ActivityHoldReason.OTHER: (
            "Otro"
        ),
    }

    @classmethod
    def present(
        cls,
        result: ListWorkOrderActivitiesResult,
    ) -> WorkOrderActivitiesViewModel:

        items = []

        for item in result.items:

            active_hold = item.active_hold
            hold_history = []

            for history_item in item.hold_history:

                hold = history_item.hold

                duration_minutes = None

                if hold.resumed_at is not None:
                    duration_seconds = (
                        hold.resumed_at
                        - hold.held_at
                    ).total_seconds()

                    duration_minutes = int(
                        duration_seconds // 60
                    )

                hold_history.append(
                    ActivityHoldHistoryItemViewModel(
                        code=hold.code,
                        reason=hold.reason.value,
                        reason_label=(
                            cls.HOLD_REASON_LABELS[
                                hold.reason
                            ]
                        ),
                        observations=(
                            hold.observations
                        ),
                        held_at=cls._format_datetime(
                            hold.held_at
                        ),
                        held_by_person_code=(
                            hold.held_by_person_code
                        ),
                        held_by_person_name=(
                            history_item.held_by_person.name
                            if history_item.held_by_person
                            else None
                        ),
                        resumed_at=(
                            cls._format_datetime(
                                hold.resumed_at
                            )
                        ),
                        resumed_by_person_code=(
                            hold.resumed_by_person_code
                        ),
                        resumed_by_person_name=(
                            history_item.resumed_by_person.name
                            if history_item.resumed_by_person
                            else None
                        ),
                        duration_minutes=(
                            duration_minutes
                        ),
                        is_active=hold.is_active,
                    )
                )
            items.append(
                WorkOrderActivityItemViewModel(
                    code=item.activity.code,
                    title=item.activity.title,
                    description=(
                        item.activity.description
                    ),
                    responsible_person_code=(
                        item.responsible_person.code
                    ),
                    responsible_person_name=(
                        item.responsible_person.name
                    ),
                    status=(
                        item.activity.status.value
                    ),
                    status_label=(
                        cls.STATUS_LABELS[
                            item.activity.status
                        ]
                    ),
                    estimated_minutes=(
                        item.activity.estimated_minutes
                    ),
                    actual_minutes=(
                        item.activity.actual_minutes
                    ),
                    started_at=cls._format_datetime(
                        item.activity.started_at
                    ),
                    completed_at=cls._format_datetime(
                        item.activity.completed_at
                    ),
                    hold_reason=(
                        active_hold.reason.value
                        if active_hold
                        else None
                    ),
                    hold_reason_label=(
                        cls.HOLD_REASON_LABELS[
                            active_hold.reason
                        ]
                        if active_hold
                        else None
                    ),
                    hold_observations=(
                        active_hold.observations
                        if active_hold
                        else None
                    ),
                    held_at=(
                        cls._format_datetime(
                            active_hold.held_at
                        )
                        if active_hold
                        else None
                    ),
                    held_by_person_code=(
                        active_hold.held_by_person_code
                        if active_hold
                        else None
                    ),
                    held_by_person_name=(
                        item.held_by_person.name
                        if item.held_by_person
                        else None
                    ),
                    hold_history=hold_history,
                )
            )

        return WorkOrderActivitiesViewModel(
            items=items
        )

    @staticmethod
    def _format_datetime(
        value,
    ) -> str | None:

        if value is None:
            return None

        return value.strftime(
            "%d/%m/%Y %H:%M"
        )

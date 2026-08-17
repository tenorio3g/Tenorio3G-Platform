from app.domains.work_orders.activities.use_cases import (
    ListWorkOrderActivitiesResult,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from .work_order_activities_view_model import (
    WorkOrderActivitiesViewModel,
    WorkOrderActivityItemViewModel,
)


class WorkOrderActivitiesPresenter:

    STATUS_LABELS = {
        ActivityStatus.PENDING: "Pendiente",
        ActivityStatus.IN_PROGRESS: "En proceso",
        ActivityStatus.COMPLETED: "Finalizada",
    }

    @classmethod
    def present(
        cls,
        result: ListWorkOrderActivitiesResult,
    ) -> WorkOrderActivitiesViewModel:

        items = [
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
            )
            for item in result.items
        ]

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
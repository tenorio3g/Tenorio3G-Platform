from app.domains.work_orders.value_objects import (
    WorkOrderStatus,
)

from app.domains.work_orders.activities.value_objects import (
    ActivityStatus,
)

from .dashboard_view_model import (
    DashboardRecentWorkOrderViewModel,
    DashboardViewModel,
)


class DashboardService:

    def __init__(
        self,
        asset_repository,
        work_order_repository,
        person_repository,
        activity_repository,
    ):
        self._asset_repository = asset_repository
        self._work_order_repository = (
            work_order_repository
        )
        self._person_repository = (
            person_repository
        )
        self._activity_repository = (
            activity_repository
        )

    def build(
        self,
    ) -> DashboardViewModel:

        assets = (
            self._asset_repository.find_all()
        )

        work_orders = (
            self._work_order_repository.list_all()
        )

        people = (
            self._person_repository.list_all()
        )

        activities = []

        for work_order in work_orders:

            activities.extend(
                self._activity_repository
                .list_by_work_order(
                    work_order.code
                )
            )

        active_people = sum(
            1
            for person in people
            if person.is_active
        )

        pending_activities = sum(
            1
            for activity in activities
            if activity.status
            == ActivityStatus.PENDING
        )

        def count_status(
            status,
        ):
            return sum(
                1
                for work_order in work_orders
                if work_order.status == status
            )

        ordered_work_orders = sorted(
            work_orders,
            key=lambda work_order: (
                work_order.created_at
            ),
            reverse=True,
        )

        recent_work_orders = [
            DashboardRecentWorkOrderViewModel(
                code=work_order.code,
                title=work_order.title,
                status=work_order.status.value,
                priority=work_order.priority,
                asset_code=work_order.asset_code,
                created_at=(
                    work_order.created_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
            )
            for work_order
            in ordered_work_orders[:5]
        ]

        return DashboardViewModel(
            total_assets=len(assets),
            total_work_orders=len(work_orders),
            active_people=active_people,
            pending_activities=pending_activities,

            created_work_orders=count_status(
                WorkOrderStatus.CREATED
            ),

            assigned_work_orders=count_status(
                WorkOrderStatus.ASSIGNED
            ),

            in_progress_work_orders=count_status(
                WorkOrderStatus.IN_PROGRESS
            ),

            on_hold_work_orders=count_status(
                WorkOrderStatus.ON_HOLD
            ),

            completed_work_orders=count_status(
                WorkOrderStatus.COMPLETED
            ),

            closed_work_orders=count_status(
                WorkOrderStatus.CLOSED
            ),

            cancelled_work_orders=count_status(
                WorkOrderStatus.CANCELLED
            ),

            recent_work_orders=recent_work_orders,
        )
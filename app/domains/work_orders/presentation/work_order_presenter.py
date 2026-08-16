from app.domains.work_orders.entities import (
    WorkOrder,
)

from .work_order_view_model import (
    WorkOrderViewModel,
)


class WorkOrderPresenter:

    @staticmethod
    def present(
        work_order: WorkOrder,
    ) -> WorkOrderViewModel:

        return WorkOrderViewModel(
            code=work_order.code,
            title=work_order.title,
            description=work_order.description,
            work_type=work_order.work_type,
            priority=work_order.priority,
            asset_code=work_order.asset_code,
            requester_person_code=(
                work_order.requester_person_code
            ),
            supervisor_person_code=(
                work_order.supervisor_person_code
            ),
            status=work_order.status.value,
            created_at=(
                work_order.created_at.strftime(
                    "%d/%m/%Y %H:%M"
                )
            ),
        )
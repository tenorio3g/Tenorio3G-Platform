from app.domains.work_orders.tools.use_cases import (
    ListWorkOrderToolsResult,
)

from .work_order_tools_view_model import (
    WorkOrderToolItemViewModel,
    WorkOrderToolsViewModel,
)


class WorkOrderToolsPresenter:

    @staticmethod
    def present(
        result: ListWorkOrderToolsResult,
    ) -> WorkOrderToolsViewModel:

        items = [
            WorkOrderToolItemViewModel(
                usage_id=item.usage_id,
                tool_code=item.tool_code,
                tool_name=item.tool_name,
                quantity=item.quantity,
                status=item.status.value,
                status_label=(
                    "Prestada"
                    if item.status.value == "ISSUED"
                    else "Devuelta"
                ),
                issued_at=(
                    item.issued_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
                returned_at=(
                    item.returned_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                    if item.returned_at
                    else None
                ),
                observations=item.observations,
            )
            for item in result.items
        ]

        return WorkOrderToolsViewModel(
            items=items
        )
from app.domains.work_orders.materials.use_cases import (
    ListWorkOrderSparePartsResult,
)

from .work_order_spare_parts_view_model import (
    WorkOrderSparePartItemViewModel,
    WorkOrderSparePartsViewModel,
)


class WorkOrderSparePartsPresenter:

    @staticmethod
    def present(
        result: ListWorkOrderSparePartsResult,
    ) -> WorkOrderSparePartsViewModel:

        items = [
            WorkOrderSparePartItemViewModel(
                code=item.spare_part.code,
                name=item.spare_part.name,
                manufacturer=(
                    item.spare_part.manufacturer
                    or "Sin fabricante"
                ),
                part_number=(
                    item.spare_part.part_number
                    or "Sin número de parte"
                ),
                unit=(
                    item.spare_part.unit
                    or "pieza"
                ),
                quantity=item.usage.quantity,
                unit_cost=item.usage.unit_cost,
                total_cost=item.usage.total_cost,
                used_at=(
                    item.usage.used_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
                observations=(
                    item.usage.observations
                ),
            )
            for item in result.items
        ]

        return WorkOrderSparePartsViewModel(
            items=items
        )
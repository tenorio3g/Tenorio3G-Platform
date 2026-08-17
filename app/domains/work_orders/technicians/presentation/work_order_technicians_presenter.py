from app.domains.work_orders.technicians.use_cases import (
    ListWorkOrderTechniciansResult,
)

from .work_order_technicians_view_model import (
    WorkOrderTechnicianItemViewModel,
    WorkOrderTechniciansViewModel,
)


class WorkOrderTechniciansPresenter:

    @staticmethod
    def present(
        result: ListWorkOrderTechniciansResult,
    ) -> WorkOrderTechniciansViewModel:

        ordered_items = sorted(
            result.items,
            key=lambda item: (
                item.person.name.lower()
            ),
        )

        items = [
            WorkOrderTechnicianItemViewModel(
                person_code=(
                    item.person.code
                ),
                name=(
                    item.person.name
                ),
                position=(
                    item.person.position
                    or "Sin puesto registrado"
                ),
                assigned_at=(
                    item.assignment.assigned_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
            )
            for item in ordered_items
        ]

        return WorkOrderTechniciansViewModel(
            items=items
        )
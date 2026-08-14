from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from .preventive_maintenance_view_model import (
    PreventiveMaintenanceItemViewModel,
    PreventiveMaintenanceViewModel,
)


class PreventiveMaintenancePresenter:

    @staticmethod
    def present(
        plans: list[PreventiveMaintenancePlan],
        reference_at: datetime,
    ) -> PreventiveMaintenanceViewModel:

        ordered_plans = sorted(
            plans,
            key=lambda plan: plan.next_due_at,
        )

        items = [
            PreventiveMaintenanceItemViewModel(
                code=plan.code,
                title=plan.title,
                frequency_days=plan.frequency_days,
                responsible_person_code=(
                    plan.responsible_person_code
                ),
                next_due_at=(
                    plan.next_due_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
                status=(
                    PreventiveMaintenancePresenter
                    ._resolve_status(
                        plan,
                        reference_at,
                    )
                ),
                is_active=plan.is_active,
            )
            for plan in ordered_plans
        ]

        return PreventiveMaintenanceViewModel(
            items=items
        )

    @staticmethod
    def _resolve_status(
        plan: PreventiveMaintenancePlan,
        reference_at: datetime,
    ) -> str:

        if not plan.is_active:
            return "INACTIVO"

        if (
            plan.next_due_at.date()
            < reference_at.date()
        ):
            return "VENCIDO"

        if (
            plan.next_due_at.date()
            == reference_at.date()
        ):
            return "HOY"

        return "PROGRAMADO"
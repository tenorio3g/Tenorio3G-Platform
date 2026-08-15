from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
    PreventiveMaintenancePlan,
)

from .preventive_maintenance_metrics_view_model import (
    PreventiveMaintenanceMetricsViewModel,
)


class PreventiveMaintenanceMetricsPresenter:

    @staticmethod
    def present(
        plans: list[PreventiveMaintenancePlan],
        executions: list[PreventiveMaintenanceExecution],
        reference_at: datetime,
    ) -> PreventiveMaintenanceMetricsViewModel:

        active_plans = 0
        programmed = 0
        due_today = 0
        overdue = 0
        inactive = 0

        for plan in plans:

            if not plan.is_active:
                inactive += 1
                continue

            active_plans += 1

            if (
                plan.next_due_at.date()
                < reference_at.date()
            ):
                overdue += 1

            elif (
                plan.next_due_at.date()
                == reference_at.date()
            ):
                due_today += 1

            else:
                programmed += 1

        on_time_executions = sum(
            1
            for execution in executions
            if execution.is_on_time()
        )

        late_executions = sum(
            1
            for execution in executions
            if execution.is_late()
        )

        evaluated_executions = (
            on_time_executions
            + late_executions
        )

        compliance_percent = (
            round(
                (
                    on_time_executions
                    / evaluated_executions
                )
                * 100,
                2,
            )
            if evaluated_executions > 0
            else 0.0
        )

        return PreventiveMaintenanceMetricsViewModel(
            total_plans=len(plans),
            active_plans=active_plans,
            programmed=programmed,
            due_today=due_today,
            overdue=overdue,
            inactive=inactive,
            executions=len(executions),
            on_time_executions=on_time_executions,
            late_executions=late_executions,
            compliance_percent=compliance_percent,
        )
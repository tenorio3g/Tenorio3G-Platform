from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
)

from .preventive_maintenance_executions_view_model import (
    PreventiveMaintenanceExecutionItemViewModel,
    PreventiveMaintenanceExecutionsViewModel,
)


class PreventiveMaintenanceExecutionsPresenter:

    @staticmethod
    def present(
        executions: list[
            PreventiveMaintenanceExecution
        ],
    ) -> PreventiveMaintenanceExecutionsViewModel:

        ordered_executions = sorted(
            executions,
            key=lambda execution: execution.completed_at,
            reverse=True,
        )

        items = [
            PreventiveMaintenanceExecutionItemViewModel(
                code=execution.code,
                plan_code=execution.plan_code,
                performed_by=execution.performed_by,
                scheduled_at=(
                    execution.scheduled_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
                
                completed_at=(
                    execution.completed_at.strftime(
                        "%d/%m/%Y %H:%M"
                    )
                ),
                status=(
                    "A TIEMPO"
                    if execution.is_on_time()
                    else "ATRASADO"
                ),
                observations=(
                    execution.observations
                    or "Sin observaciones."
                ),
            )
            for execution in ordered_executions
        ]

        return PreventiveMaintenanceExecutionsViewModel(
            items=items
        )
from dataclasses import dataclass
from datetime import datetime, timedelta

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenanceExecution,
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    PreventiveMaintenanceExecutionRepository,
    PreventiveMaintenanceRepository,
)


@dataclass(frozen=True)
class CompletePreventiveMaintenancePlanCommand:
    execution_code: str
    plan_code: str
    performed_by: str
    completed_at: datetime
    observations: str = ""


@dataclass(frozen=True)
class CompletePreventiveMaintenancePlanResult:
    execution: PreventiveMaintenanceExecution
    plan: PreventiveMaintenancePlan


class CompletePreventiveMaintenancePlan:

    def __init__(
        self,
        plan_repository: PreventiveMaintenanceRepository,
        execution_repository: PreventiveMaintenanceExecutionRepository,
    ):
        self._plan_repository = plan_repository
        self._execution_repository = execution_repository

    def execute(
        self,
        command: CompletePreventiveMaintenancePlanCommand,
    ) -> CompletePreventiveMaintenancePlanResult:

        plan = self._plan_repository.get_by_code(
            command.plan_code
        )

        if plan is None:
            raise ValueError(
                "preventive maintenance plan not found"
            )

        if not plan.is_active:
            raise ValueError(
                "preventive maintenance plan is inactive"
            )

        existing_execution = (
            self._execution_repository.get_by_code(
                command.execution_code
            )
        )

        if existing_execution is not None:
            raise ValueError(
                "preventive maintenance execution already exists"
            )

        execution = PreventiveMaintenanceExecution(
            code=command.execution_code,
            plan_code=plan.code,
            asset_code=plan.asset_code,
            performed_by=command.performed_by,
            scheduled_at=plan.next_due_at,
            completed_at=command.completed_at,
            observations=command.observations,
        )

        schedule_base = (
            plan.next_due_at
            if command.completed_at <= plan.next_due_at
            else command.completed_at
        )

        next_due_at = (
            schedule_base
            + timedelta(
                days=plan.frequency_days
            )
        )

        updated_plan = PreventiveMaintenancePlan(
            code=plan.code,
            asset_code=plan.asset_code,
            title=plan.title,
            frequency_days=plan.frequency_days,
            responsible_person_code=(
                plan.responsible_person_code
            ),
            next_due_at=next_due_at,
            description=plan.description,
            is_active=plan.is_active,
        )

        self._execution_repository.save(
            execution
        )

        self._plan_repository.save(
            updated_plan
        )

        return CompletePreventiveMaintenancePlanResult(
            execution=execution,
            plan=updated_plan,
        )
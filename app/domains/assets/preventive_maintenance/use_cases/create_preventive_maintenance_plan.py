from dataclasses import dataclass
from datetime import datetime

from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from app.domains.assets.preventive_maintenance.repositories import (
    PreventiveMaintenanceRepository,
)


@dataclass(frozen=True)
class CreatePreventiveMaintenancePlanCommand:
    code: str
    asset_code: str
    title: str
    frequency_days: int
    responsible_person_code: str
    next_due_at: datetime
    description: str = ""
    is_active: bool = True


@dataclass(frozen=True)
class CreatePreventiveMaintenancePlanResult:
    plan: PreventiveMaintenancePlan


class CreatePreventiveMaintenancePlan:

    def __init__(
        self,
        repository: PreventiveMaintenanceRepository,
    ):
        self._repository = repository

    def execute(
        self,
        command: CreatePreventiveMaintenancePlanCommand,
    ) -> CreatePreventiveMaintenancePlanResult:

        existing = self._repository.get_by_code(
            command.code
        )

        if existing is not None:
            raise ValueError(
                "preventive maintenance plan already exists"
            )

        plan = PreventiveMaintenancePlan(
            code=command.code,
            asset_code=command.asset_code,
            title=command.title,
            frequency_days=command.frequency_days,
            responsible_person_code=(
                command.responsible_person_code
            ),
            next_due_at=command.next_due_at,
            description=command.description,
            is_active=command.is_active,
        )

        self._repository.save(
            plan
        )

        return CreatePreventiveMaintenancePlanResult(
            plan=plan
        )
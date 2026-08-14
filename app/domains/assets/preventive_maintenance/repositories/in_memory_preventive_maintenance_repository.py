from app.domains.assets.preventive_maintenance.entities import (
    PreventiveMaintenancePlan,
)

from .preventive_maintenance_repository import (
    PreventiveMaintenanceRepository,
)


class InMemoryPreventiveMaintenanceRepository(
    PreventiveMaintenanceRepository,
):

    def __init__(
        self,
    ):
        self._plans: dict[
            str,
            PreventiveMaintenancePlan,
        ] = {}

    def save(
        self,
        plan: PreventiveMaintenancePlan,
    ) -> None:

        self._plans[
            plan.code
        ] = plan

    def get_by_code(
        self,
        code: str,
    ) -> PreventiveMaintenancePlan | None:

        normalized_code = str(
            code
        ).strip().upper()

        return self._plans.get(
            normalized_code
        )

    def list_by_asset(
        self,
        asset_code: str,
    ) -> list[PreventiveMaintenancePlan]:

        normalized_asset_code = str(
            asset_code
        ).strip().upper()

        return [
            plan
            for plan in self._plans.values()
            if plan.asset_code
            == normalized_asset_code
        ]

    def list_all(
        self,
    ) -> list[PreventiveMaintenancePlan]:

        return list(
            self._plans.values()
        )

    def delete(
        self,
        code: str,
    ) -> None:

        normalized_code = str(
            code
        ).strip().upper()

        self._plans.pop(
            normalized_code,
            None,
        )
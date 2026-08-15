from datetime import datetime


class PreventiveMaintenanceExecution:

    def __init__(
        self,
        code,
        plan_code,
        asset_code,
        performed_by,
        scheduled_at,
        completed_at,
        observations="",
    ):

        self.code = self._required(
            code,
            "code",
        ).upper()

        self.plan_code = self._required(
            plan_code,
            "plan_code",
        ).upper()

        self.asset_code = self._required(
            asset_code,
            "asset_code",
        ).upper()

        self.performed_by = self._required(
            performed_by,
            "performed_by",
        )

        if not isinstance(
            scheduled_at,
            datetime,
        ):
            raise ValueError(
                "scheduled_at must be a datetime"
            )

        self.scheduled_at = scheduled_at

        if not isinstance(
            completed_at,
            datetime,
        ):
            raise ValueError(
                "completed_at must be a datetime"
            )

        self.completed_at = completed_at

        self.observations = str(
            observations
        ).strip()

    @staticmethod
    def _required(
        value,
        field_name,
    ) -> str:

        normalized = str(
            value
        ).strip()

        if not normalized:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized


    def is_on_time(
        self,
    ) -> bool:

        return (
            self.completed_at
            <= self.scheduled_at
        )


    def is_late(
        self,
    ) -> bool:

        return (
            self.completed_at
            > self.scheduled_at
        )
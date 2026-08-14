from datetime import datetime


class PreventiveMaintenancePlan:

    def __init__(
        self,
        code,
        asset_code,
        title,
        frequency_days,
        responsible_person_code,
        next_due_at,
        description="",
        is_active=True,
    ):
        self.code = self._required(
            code,
            "code",
        ).upper()

        self.asset_code = self._required(
            asset_code,
            "asset_code",
        ).upper()

        self.title = self._required(
            title,
            "title",
        )

        self.frequency_days = int(
            frequency_days
        )

        if self.frequency_days <= 0:
            raise ValueError(
                "frequency_days must be greater than zero"
            )

        self.responsible_person_code = (
            self._required(
                responsible_person_code,
                "responsible_person_code",
            ).upper()
        )

        if not isinstance(
            next_due_at,
            datetime,
        ):
            raise ValueError(
                "next_due_at must be a datetime"
            )

        self.next_due_at = next_due_at

        self.description = str(
            description
        ).strip()

        self.is_active = bool(
            is_active
        )

    @staticmethod
    def _required(
        value,
        field_name,
    ):
        value = str(value).strip()

        if not value:
            raise ValueError(
                f"{field_name} is required"
            )

        return value

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def is_due(
        self,
        reference_at: datetime,
    ) -> bool:

        if not self.is_active:
            return False

        return (
            self.next_due_at
            <= reference_at
        )
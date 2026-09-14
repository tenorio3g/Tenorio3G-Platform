from app.domains.work_orders.activities.holds.entities import (
    ActivityHold,
)

from .activity_hold_repository import (
    ActivityHoldRepository,
)


class InMemoryActivityHoldRepository(
    ActivityHoldRepository,
):

    def __init__(
        self,
    ):
        self._holds: dict[
            str,
            ActivityHold,
        ] = {}


    def save(
        self,
        hold: ActivityHold,
    ) -> None:

        if hold.is_active:

            existing_active_hold = (
                self.get_active_by_activity(
                    hold.activity_code
                )
            )

            if (
                existing_active_hold is not None
                and existing_active_hold.code
                != hold.code
            ):
                raise ValueError(
                    "activity already has active hold"
                )

        self._holds[
            hold.code
        ] = hold

    def get_by_code(
        self,
        code: str,
    ) -> ActivityHold | None:

        normalized_code = str(
            code
        ).strip().upper()

        return self._holds.get(
            normalized_code
        )


    def list_by_activity(
        self,
        activity_code: str,
    ) -> list[ActivityHold]:

        normalized_activity_code = str(
            activity_code
        ).strip().upper()

        return [
            hold
            for hold
            in self._holds.values()
            if hold.activity_code
            == normalized_activity_code
        ]


    def get_active_by_activity(
        self,
        activity_code: str,
    ) -> ActivityHold | None:

        normalized_activity_code = str(
            activity_code
        ).strip().upper()

        for hold in self._holds.values():

            if (
                hold.activity_code
                == normalized_activity_code
                and hold.is_active
            ):
                return hold

        return None

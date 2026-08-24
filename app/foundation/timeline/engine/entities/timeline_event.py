from datetime import datetime


class TimelineEvent:

    def __init__(
        self,
        event_id,
        entity_type,
        entity_code,
        event_type,
        title,
        actor_person_code,
        occurred_at,
        description="",
        reference_type=None,
        reference_code=None,
        actor_name=None,
    ):
        self.event_id = self._required(
            event_id,
            "event_id",
        ).upper()

        self.entity_type = self._required(
            entity_type,
            "entity_type",
        ).upper()

        self.entity_code = self._required(
            entity_code,
            "entity_code",
        ).upper()

        self.event_type = self._required(
            event_type,
            "event_type",
        ).upper()

        self.title = self._required(
            title,
            "title",
        )

        self.actor_person_code = (
            self._optional_upper(
                actor_person_code
            )
        )

        self.actor_name = self._optional(
            actor_name
        )

        if (
            self.actor_person_code is None
            and self.actor_name is None
        ):
            raise ValueError(
                "actor_person_code or actor_name is required"
            )

        if not isinstance(
            occurred_at,
            datetime,
        ):
            raise ValueError(
                "occurred_at must be a datetime"
            )

        self.occurred_at = occurred_at

        self.description = str(
            description or ""
        ).strip()

        self.reference_type = (
            self._optional_upper(
                reference_type
            )
        )

        self.reference_code = (
            self._optional_upper(
                reference_code
            )
        )

    @staticmethod
    def _required(
        value,
        field_name,
    ) -> str:

        normalized = str(
            value or ""
        ).strip()

        if not normalized:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized

    @staticmethod
    def _optional(
        value,
    ) -> str | None:

        if value is None:
            return None

        normalized = str(
            value
        ).strip()

        if not normalized:
            return None

        return normalized

    @staticmethod
    def _optional_upper(
        value,
    ) -> str | None:

        normalized = TimelineEvent._optional(
            value
        )

        if normalized is None:
            return None

        return normalized.upper()

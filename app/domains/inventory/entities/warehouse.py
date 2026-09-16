class Warehouse:

    def __init__(
        self,
        code: str,
        name: str,
        description: str = "",
        is_active: bool = True,
    ) -> None:

        self.code = self._normalize_required_code(
            code,
            "code",
        )

        self.name = self._normalize_required_text(
            name,
            "name",
        )

        self.description = str(
            description or ""
        ).strip()

        if not isinstance(
            is_active,
            bool,
        ):
            raise ValueError(
                "is_active must be bool"
            )

        self.is_active = is_active

    def deactivate(
        self,
    ) -> None:

        self.is_active = False

    def activate(
        self,
    ) -> None:

        self.is_active = True

    @staticmethod
    def _normalize_required_code(
        value: str,
        field_name: str,
    ) -> str:

        normalized_value = str(
            value
        ).strip().upper()

        if not normalized_value:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized_value

    @staticmethod
    def _normalize_required_text(
        value: str,
        field_name: str,
    ) -> str:

        normalized_value = str(
            value
        ).strip()

        if not normalized_value:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized_value

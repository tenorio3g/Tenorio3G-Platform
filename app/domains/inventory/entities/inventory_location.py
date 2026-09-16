class InventoryLocation:

    def __init__(
        self,
        code: str,
        warehouse_code: str,
        name: str,
        aisle: str = "",
        rack: str = "",
        level: str = "",
        bin: str = "",
        description: str = "",
        is_active: bool = True,
    ) -> None:

        self.code = self._normalize_required_code(
            code,
            "code",
        )

        self.warehouse_code = (
            self._normalize_required_code(
                warehouse_code,
                "warehouse_code",
            )
        )

        self.name = self._normalize_required_text(
            name,
            "name",
        )

        self.aisle = self._normalize_optional_text(
            aisle
        )

        self.rack = self._normalize_optional_text(
            rack
        )

        self.level = self._normalize_optional_text(
            level
        )

        self.bin = self._normalize_optional_text(
            bin
        )

        self.description = (
            self._normalize_optional_text(
                description
            )
        )

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

    @staticmethod
    def _normalize_optional_text(
        value,
    ) -> str:

        return str(
            value or ""
        ).strip()

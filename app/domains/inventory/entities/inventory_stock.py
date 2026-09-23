import math


class InventoryStock:

    def __init__(
        self,
        spare_part_code: str,
        location_code: str,
        quantity: float = 0,
    ) -> None:

        self.spare_part_code = (
            self._normalize_required_code(
                spare_part_code,
                "spare_part_code",
            )
        )

        self.location_code = (
            self._normalize_required_code(
                location_code,
                "location_code",
            )
        )

        self.quantity = (
            self._validate_non_negative(
                quantity,
                "quantity",
            )
        )

    @property
    def is_out_of_stock(
        self,
    ) -> bool:

        return self.quantity == 0

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
    def _validate_non_negative(
        value,
        field_name: str,
    ) -> float:

        try:
            normalized_value = float(
                value
            )
        except (
            TypeError,
            ValueError,
        ) as exc:
            raise ValueError(
                f"{field_name} must be numeric"
            ) from exc

        if not math.isfinite(
            normalized_value
        ):
            raise ValueError(
                f"{field_name} must be finite"
            )

        if normalized_value < 0:
            raise ValueError(
                f"{field_name} cannot be negative"
            )

        return normalized_value

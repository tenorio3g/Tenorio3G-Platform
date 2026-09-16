import math


class InventoryStock:

    def __init__(
        self,
        spare_part_code: str,
        location_code: str,
        quantity: float = 0,
        minimum_stock: float = 0,
        maximum_stock: float = 0,
        reorder_point: float = 0,
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

        self.quantity = self._validate_non_negative(
            quantity,
            "quantity",
        )

        self.minimum_stock = (
            self._validate_non_negative(
                minimum_stock,
                "minimum_stock",
            )
        )

        self.maximum_stock = (
            self._validate_non_negative(
                maximum_stock,
                "maximum_stock",
            )
        )

        self.reorder_point = (
            self._validate_non_negative(
                reorder_point,
                "reorder_point",
            )
        )

        if (
            self.maximum_stock > 0
            and self.maximum_stock
            < self.minimum_stock
        ):
            raise ValueError(
                "maximum_stock cannot be below "
                "minimum_stock"
            )

    @property
    def is_out_of_stock(
        self,
    ) -> bool:

        return self.quantity == 0

    @property
    def is_below_minimum(
        self,
    ) -> bool:

        return (
            self.quantity
            < self.minimum_stock
        )

    @property
    def needs_reorder(
        self,
    ) -> bool:

        return (
            self.quantity
            <= self.reorder_point
        )

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

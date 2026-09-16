import math

from datetime import datetime
from enum import Enum


class InventoryMovementType(str, Enum):

    RECEIPT = "RECEIPT"
    ISSUE_TO_WORK_ORDER = "ISSUE_TO_WORK_ORDER"
    RETURN_FROM_WORK_ORDER = "RETURN_FROM_WORK_ORDER"
    ADJUSTMENT_IN = "ADJUSTMENT_IN"
    ADJUSTMENT_OUT = "ADJUSTMENT_OUT"
    TRANSFER_OUT = "TRANSFER_OUT"
    TRANSFER_IN = "TRANSFER_IN"


class InventoryMovement:

    def __init__(
        self,
        code: str,
        movement_type: InventoryMovementType,
        spare_part_code: str,
        quantity: float,
        actor_person_code: str,
        occurred_at: datetime,
        source_location_code=None,
        target_location_code=None,
        quantity_before: float = 0,
        quantity_after: float = 0,
        work_order_code=None,
        activity_code=None,
        observations: str = "",
        transfer_code=None,
    ) -> None:

        self.code = self._normalize_required_code(
            code,
            "code",
        )

        self.movement_type = (
            self._validate_movement_type(
                movement_type
            )
        )

        self.spare_part_code = (
            self._normalize_required_code(
                spare_part_code,
                "spare_part_code",
            )
        )

        self.quantity = (
            self._validate_positive_number(
                quantity,
                "quantity",
            )
        )

        self.source_location_code = (
            self._normalize_optional_code(
                source_location_code
            )
        )

        self.target_location_code = (
            self._normalize_optional_code(
                target_location_code
            )
        )

        self.quantity_before = (
            self._validate_non_negative_number(
                quantity_before,
                "quantity_before",
            )
        )

        self.quantity_after = (
            self._validate_non_negative_number(
                quantity_after,
                "quantity_after",
            )
        )

        self.work_order_code = (
            self._normalize_optional_code(
                work_order_code
            )
        )

        self.activity_code = (
            self._normalize_optional_code(
                activity_code
            )
        )

        self.actor_person_code = (
            self._normalize_required_code(
                actor_person_code,
                "actor_person_code",
            )
        )

        if not isinstance(
            occurred_at,
            datetime,
        ):
            raise ValueError(
                "occurred_at must be datetime"
            )

        self.occurred_at = occurred_at

        self.observations = str(
            observations or ""
        ).strip()

        self.transfer_code = (
            self._normalize_optional_code(
                transfer_code
            )
        )

        self._validate_movement_rules()
        self._validate_balance_consistency()

    def _validate_movement_rules(
        self,
    ) -> None:

        if (
            self.movement_type
            == InventoryMovementType.RECEIPT
        ):
            self._require_target_location()

        elif (
            self.movement_type
            == InventoryMovementType.ISSUE_TO_WORK_ORDER
        ):
            self._require_source_location()
            self._require_work_order()

        elif (
            self.movement_type
            == InventoryMovementType.RETURN_FROM_WORK_ORDER
        ):
            self._require_target_location()
            self._require_work_order()

        elif (
            self.movement_type
            == InventoryMovementType.ADJUSTMENT_IN
        ):
            self._require_target_location()
            self._require_observations()

        elif (
            self.movement_type
            == InventoryMovementType.ADJUSTMENT_OUT
        ):
            self._require_source_location()
            self._require_observations()

        elif (
            self.movement_type
            == InventoryMovementType.TRANSFER_OUT
        ):
            self._require_source_location()
            self._require_transfer_code()

        elif (
            self.movement_type
            == InventoryMovementType.TRANSFER_IN
        ):
            self._require_target_location()
            self._require_transfer_code()

    def _validate_balance_consistency(
        self,
    ) -> None:

        incoming_types = {
            InventoryMovementType.RECEIPT,
            InventoryMovementType.RETURN_FROM_WORK_ORDER,
            InventoryMovementType.ADJUSTMENT_IN,
            InventoryMovementType.TRANSFER_IN,
        }

        outgoing_types = {
            InventoryMovementType.ISSUE_TO_WORK_ORDER,
            InventoryMovementType.ADJUSTMENT_OUT,
            InventoryMovementType.TRANSFER_OUT,
        }

        if self.movement_type in incoming_types:
            expected_quantity_after = (
                self.quantity_before
                + self.quantity
            )

        elif self.movement_type in outgoing_types:
            expected_quantity_after = (
                self.quantity_before
                - self.quantity
            )

        else:
            return

        if not math.isclose(
            self.quantity_after,
            expected_quantity_after,
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            raise ValueError(
                "quantity_after is inconsistent "
                "with movement"
            )

    def _require_transfer_code(
        self,
    ) -> None:

        if not self.transfer_code:
            raise ValueError(
                "transfer_code is required "
                f"for {self.movement_type.value}"
            )

    def _require_observations(
        self,
    ) -> None:

        if not self.observations:
            raise ValueError(
                "observations is required "
                f"for {self.movement_type.value}"
            )

    def _require_source_location(
        self,
    ) -> None:

        if not self.source_location_code:
            raise ValueError(
                "source_location_code is required "
                f"for {self.movement_type.value}"
            )

    def _require_target_location(
        self,
    ) -> None:

        if not self.target_location_code:
            raise ValueError(
                "target_location_code is required "
                f"for {self.movement_type.value}"
            )

    def _require_work_order(
        self,
    ) -> None:

        if not self.work_order_code:
            raise ValueError(
                "work_order_code is required "
                f"for {self.movement_type.value}"
            )

    @staticmethod
    def _validate_movement_type(
        value,
    ) -> InventoryMovementType:

        if not isinstance(
            value,
            InventoryMovementType,
        ):
            raise ValueError(
                "movement_type must be "
                "InventoryMovementType"
            )

        return value

    @staticmethod
    def _normalize_required_code(
        value,
        field_name: str,
    ) -> str:

        normalized_value = str(
            value or ""
        ).strip().upper()

        if not normalized_value:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized_value

    @staticmethod
    def _normalize_optional_code(
        value,
    ):

        if value is None:
            return None

        normalized_value = str(
            value
        ).strip().upper()

        if not normalized_value:
            return None

        return normalized_value

    @staticmethod
    def _validate_positive_number(
        value,
        field_name: str,
    ) -> float:

        normalized_value = (
            InventoryMovement
            ._normalize_number(
                value,
                field_name,
            )
        )

        if normalized_value <= 0:
            raise ValueError(
                f"{field_name} must be "
                "greater than zero"
            )

        return normalized_value

    @staticmethod
    def _validate_non_negative_number(
        value,
        field_name: str,
    ) -> float:

        normalized_value = (
            InventoryMovement
            ._normalize_number(
                value,
                field_name,
            )
        )

        if normalized_value < 0:
            raise ValueError(
                f"{field_name} cannot be negative"
            )

        return normalized_value

    @staticmethod
    def _normalize_number(
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

        return normalized_value

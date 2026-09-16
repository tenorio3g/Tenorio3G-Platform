from app.domains.inventory.entities import (
    InventoryMovement,
)

from .inventory_movement_repository import (
    InventoryMovementRepository,
)


class InMemoryInventoryMovementRepository(
    InventoryMovementRepository,
):

    def __init__(
        self,
    ) -> None:
        self._movements: dict[
            str,
            InventoryMovement,
        ] = {}

    def save(
        self,
        movement: InventoryMovement,
    ) -> None:
        self._movements[
            movement.code
        ] = movement

    def get_by_code(
        self,
        code: str,
    ) -> InventoryMovement | None:

        normalized_code = self._normalize_code(
            code
        )

        return self._movements.get(
            normalized_code
        )

    def list_by_spare_part(
        self,
        spare_part_code: str,
    ) -> list[InventoryMovement]:

        normalized_code = self._normalize_code(
            spare_part_code
        )

        return self._sorted(
            [
                movement
                for movement
                in self._movements.values()
                if (
                    movement.spare_part_code
                    == normalized_code
                )
            ]
        )

    def list_by_location(
        self,
        location_code: str,
    ) -> list[InventoryMovement]:

        normalized_code = self._normalize_code(
            location_code
        )

        return self._sorted(
            [
                movement
                for movement
                in self._movements.values()
                if (
                    movement.source_location_code
                    == normalized_code
                    or
                    movement.target_location_code
                    == normalized_code
                )
            ]
        )

    def list_by_work_order(
        self,
        work_order_code: str,
    ) -> list[InventoryMovement]:

        normalized_code = self._normalize_code(
            work_order_code
        )

        return self._sorted(
            [
                movement
                for movement
                in self._movements.values()
                if (
                    movement.work_order_code
                    == normalized_code
                )
            ]
        )

    def list_by_transfer_code(
        self,
        transfer_code: str,
    ) -> list[InventoryMovement]:

        normalized_code = self._normalize_code(
            transfer_code
        )

        return self._sorted(
            [
                movement
                for movement
                in self._movements.values()
                if (
                    movement.transfer_code
                    == normalized_code
                )
            ]
        )

    @staticmethod
    def _normalize_code(
        value: str,
    ) -> str:
        return (
            str(value)
            .strip()
            .upper()
        )

    @staticmethod
    def _sorted(
        movements: list[InventoryMovement],
    ) -> list[InventoryMovement]:

        return sorted(
            movements,
            key=lambda movement: (
                movement.occurred_at,
                movement.code,
            ),
        )

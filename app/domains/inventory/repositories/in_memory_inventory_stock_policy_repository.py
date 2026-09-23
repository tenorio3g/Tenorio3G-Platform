from app.domains.inventory.entities import (
    InventoryStockPolicy,
)

from .inventory_stock_policy_repository import (
    InventoryStockPolicyRepository,
)


class InMemoryInventoryStockPolicyRepository(
    InventoryStockPolicyRepository,
):

    def __init__(
        self,
    ) -> None:

        self._policies: dict[
            tuple[str, str],
            InventoryStockPolicy,
        ] = {}

    def save(
        self,
        policy: InventoryStockPolicy,
    ) -> None:

        key = (
            policy.spare_part_code,
            policy.warehouse_code,
        )

        self._policies[key] = policy

    def get(
        self,
        spare_part_code: str,
        warehouse_code: str,
    ) -> InventoryStockPolicy | None:

        key = (
            self._normalize_code(
                spare_part_code
            ),
            self._normalize_code(
                warehouse_code
            ),
        )

        return self._policies.get(key)

    def list_by_spare_part(
        self,
        spare_part_code: str,
    ) -> list[InventoryStockPolicy]:

        normalized_code = (
            self._normalize_code(
                spare_part_code
            )
        )

        return [
            policy
            for policy
            in self._policies.values()
            if (
                policy.spare_part_code
                == normalized_code
            )
        ]

    def list_by_warehouse(
        self,
        warehouse_code: str,
    ) -> list[InventoryStockPolicy]:

        normalized_code = (
            self._normalize_code(
                warehouse_code
            )
        )

        return [
            policy
            for policy
            in self._policies.values()
            if (
                policy.warehouse_code
                == normalized_code
            )
        ]

    @staticmethod
    def _normalize_code(
        value: str,
    ) -> str:

        return (
            str(value)
            .strip()
            .upper()
        )

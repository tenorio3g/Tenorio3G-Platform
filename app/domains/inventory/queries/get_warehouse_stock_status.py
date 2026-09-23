from app.domains.inventory.queries.get_warehouse_stock import (
    GetWarehouseStock,
)
from app.domains.inventory.repositories.inventory_stock_policy_repository import (
    InventoryStockPolicyRepository,
)
from app.domains.inventory.results.warehouse_stock_status_result import (
    WarehouseStockStatusResult,
)


class GetWarehouseStockStatus:

    def __init__(
        self,
        warehouse_stock_query: GetWarehouseStock,
        policy_repository: InventoryStockPolicyRepository,
    ) -> None:

        self._warehouse_stock_query = (
            warehouse_stock_query
        )

        self._policy_repository = (
            policy_repository
        )

    def execute(
        self,
        spare_part_code: str,
        warehouse_code: str,
    ) -> WarehouseStockStatusResult:

        warehouse_stock = (
            self._warehouse_stock_query.execute(
                spare_part_code=spare_part_code,
                warehouse_code=warehouse_code,
            )
        )

        policy = self._policy_repository.get(
            warehouse_stock.spare_part_code,
            warehouse_stock.warehouse_code,
        )

        if policy is None:
            return WarehouseStockStatusResult(
                spare_part_code=(
                    warehouse_stock.spare_part_code
                ),
                warehouse_code=(
                    warehouse_stock.warehouse_code
                ),
                total_quantity=(
                    warehouse_stock.total_quantity
                ),
                locations=warehouse_stock.locations,
                policy_configured=False,
                minimum_stock=None,
                maximum_stock=None,
                reorder_point=None,
                is_below_minimum=None,
                needs_reorder=None,
            )

        total_quantity = (
            warehouse_stock.total_quantity
        )

        return WarehouseStockStatusResult(
            spare_part_code=(
                warehouse_stock.spare_part_code
            ),
            warehouse_code=(
                warehouse_stock.warehouse_code
            ),
            total_quantity=total_quantity,
            locations=warehouse_stock.locations,
            policy_configured=True,
            minimum_stock=policy.minimum_stock,
            maximum_stock=policy.maximum_stock,
            reorder_point=policy.reorder_point,
            is_below_minimum=(
                policy.is_below_minimum(
                    total_quantity
                )
            ),
            needs_reorder=(
                policy.needs_reorder(
                    total_quantity
                )
            ),
        )

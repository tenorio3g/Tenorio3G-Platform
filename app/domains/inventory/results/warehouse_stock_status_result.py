from dataclasses import dataclass

from app.domains.inventory.results.warehouse_stock_result import (
    WarehouseStockLocationResult,
)


@dataclass(frozen=True)
class WarehouseStockStatusResult:
    spare_part_code: str
    warehouse_code: str
    total_quantity: float
    locations: list[WarehouseStockLocationResult]

    policy_configured: bool

    minimum_stock: float | None
    maximum_stock: float | None
    reorder_point: float | None

    is_below_minimum: bool | None
    needs_reorder: bool | None

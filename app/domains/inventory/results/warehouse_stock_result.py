from dataclasses import dataclass


@dataclass(frozen=True)
class WarehouseStockLocationResult:
    location_code: str
    quantity: float


@dataclass(frozen=True)
class WarehouseStockResult:
    spare_part_code: str
    warehouse_code: str
    total_quantity: float
    locations: list[WarehouseStockLocationResult]

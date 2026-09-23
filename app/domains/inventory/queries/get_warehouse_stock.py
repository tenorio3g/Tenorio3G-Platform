from app.domains.inventory.repositories import (
    InventoryLocationRepository,
    InventoryStockRepository,
)

from app.domains.inventory.results import (
    WarehouseStockLocationResult,
    WarehouseStockResult,
)


class GetWarehouseStock:

    def __init__(
        self,
        location_repository: InventoryLocationRepository,
        stock_repository: InventoryStockRepository,
    ) -> None:

        self._location_repository = (
            location_repository
        )

        self._stock_repository = (
            stock_repository
        )

    def execute(
        self,
        spare_part_code: str,
        warehouse_code: str,
    ) -> WarehouseStockResult:

        normalized_spare_part_code = (
            self._normalize_required_code(
                spare_part_code,
                "spare_part_code",
            )
        )

        normalized_warehouse_code = (
            self._normalize_required_code(
                warehouse_code,
                "warehouse_code",
            )
        )

        locations = (
            self._location_repository
            .list_by_warehouse(
                normalized_warehouse_code
            )
        )

        location_codes = {
            location.code
            for location in locations
        }

        stocks = (
            self._stock_repository
            .list_by_spare_part(
                normalized_spare_part_code
            )
        )

        location_results = [
            WarehouseStockLocationResult(
                location_code=stock.location_code,
                quantity=stock.quantity,
            )
            for stock in stocks
            if (
                stock.location_code
                in location_codes
            )
        ]

        total_quantity = sum(
            item.quantity
            for item in location_results
        )

        return WarehouseStockResult(
            spare_part_code=(
                normalized_spare_part_code
            ),
            warehouse_code=(
                normalized_warehouse_code
            ),
            total_quantity=total_quantity,
            locations=location_results,
        )

    @staticmethod
    def _normalize_required_code(
        value: str,
        field_name: str,
    ) -> str:

        normalized_value = (
            str(value)
            .strip()
            .upper()
        )

        if not normalized_value:
            raise ValueError(
                f"{field_name} is required"
            )

        return normalized_value

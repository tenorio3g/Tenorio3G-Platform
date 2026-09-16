from app.domains.inventory.entities import (
    InventoryStock,
)

from .inventory_stock_repository import (
    InventoryStockRepository,
)


class InMemoryInventoryStockRepository(
    InventoryStockRepository,
):

    def __init__(
        self,
    ) -> None:
        self._stocks: dict[
            tuple[str, str],
            InventoryStock,
        ] = {}

    def save(
        self,
        stock: InventoryStock,
    ) -> None:

        key = (
            stock.spare_part_code,
            stock.location_code,
        )

        self._stocks[key] = stock

    def get(
        self,
        spare_part_code: str,
        location_code: str,
    ) -> InventoryStock | None:

        key = (
            self._normalize_code(
                spare_part_code
            ),
            self._normalize_code(
                location_code
            ),
        )

        return self._stocks.get(key)

    def list_by_spare_part(
        self,
        spare_part_code: str,
    ) -> list[InventoryStock]:

        normalized_code = self._normalize_code(
            spare_part_code
        )

        return [
            stock
            for stock in self._stocks.values()
            if (
                stock.spare_part_code
                == normalized_code
            )
        ]

    def list_by_location(
        self,
        location_code: str,
    ) -> list[InventoryStock]:

        normalized_code = self._normalize_code(
            location_code
        )

        return [
            stock
            for stock in self._stocks.values()
            if (
                stock.location_code
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

from app.domains.inventory.entities import (
    InventoryLocation,
)

from .inventory_location_repository import (
    InventoryLocationRepository,
)


class InMemoryInventoryLocationRepository(
    InventoryLocationRepository,
):

    def __init__(
        self,
    ) -> None:
        self._locations: dict[
            str,
            InventoryLocation,
        ] = {}

    def save(
        self,
        location: InventoryLocation,
    ) -> None:
        self._locations[
            location.code
        ] = location

    def get_by_code(
        self,
        code: str,
    ) -> InventoryLocation | None:

        normalized_code = (
            str(code)
            .strip()
            .upper()
        )

        return self._locations.get(
            normalized_code
        )

    def list_by_warehouse(
        self,
        warehouse_code: str,
    ) -> list[InventoryLocation]:

        normalized_warehouse_code = (
            str(warehouse_code)
            .strip()
            .upper()
        )

        return [
            location
            for location
            in self._locations.values()
            if (
                location.warehouse_code
                == normalized_warehouse_code
            )
        ]

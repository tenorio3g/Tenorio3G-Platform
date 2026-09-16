from app.domains.inventory.entities import Warehouse

from .warehouse_repository import WarehouseRepository


class InMemoryWarehouseRepository(
    WarehouseRepository,
):

    def __init__(
        self,
    ) -> None:
        self._warehouses: dict[
            str,
            Warehouse,
        ] = {}

    def save(
        self,
        warehouse: Warehouse,
    ) -> None:
        self._warehouses[
            warehouse.code
        ] = warehouse

    def get_by_code(
        self,
        code: str,
    ) -> Warehouse | None:

        normalized_code = (
            str(code)
            .strip()
            .upper()
        )

        return self._warehouses.get(
            normalized_code
        )

    def list_all(
        self,
    ) -> list[Warehouse]:
        return list(
            self._warehouses.values()
        )

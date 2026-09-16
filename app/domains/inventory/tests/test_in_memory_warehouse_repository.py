from app.domains.inventory.entities import Warehouse
from app.domains.inventory.repositories import (
    InMemoryWarehouseRepository,
)


def create_warehouse(
    code="WH-001",
    name="Almacén principal",
    description="Almacén general",
    is_active=True,
):
    return Warehouse(
        code=code,
        name=name,
        description=description,
        is_active=is_active,
    )


def test_should_save_and_get_warehouse():

    repository = InMemoryWarehouseRepository()

    warehouse = create_warehouse()

    repository.save(warehouse)

    stored = repository.get_by_code("WH-001")

    assert stored is warehouse


def test_get_by_code_should_normalize_code():

    repository = InMemoryWarehouseRepository()

    repository.save(create_warehouse())

    stored = repository.get_by_code(" wh-001 ")

    assert stored is not None
    assert stored.code == "WH-001"


def test_get_unknown_warehouse_should_return_none():

    repository = InMemoryWarehouseRepository()

    assert repository.get_by_code("WH-999") is None


def test_save_should_replace_existing_warehouse():

    repository = InMemoryWarehouseRepository()

    repository.save(
        create_warehouse(
            name="Nombre anterior",
        )
    )

    repository.save(
        create_warehouse(
            name="Nombre actualizado",
        )
    )

    stored = repository.get_by_code("WH-001")

    assert stored is not None
    assert stored.name == "Nombre actualizado"


def test_list_all_should_return_all_warehouses():

    repository = InMemoryWarehouseRepository()

    repository.save(
        create_warehouse(
            code="WH-001",
            name="Almacén principal",
        )
    )

    repository.save(
        create_warehouse(
            code="WH-002",
            name="Almacén secundario",
        )
    )

    warehouses = repository.list_all()

    assert len(warehouses) == 2
    assert {
        warehouse.code
        for warehouse in warehouses
    } == {
        "WH-001",
        "WH-002",
    }

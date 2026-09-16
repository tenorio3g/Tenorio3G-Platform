from datetime import datetime

from app.domains.inventory.entities import (
    InventoryMovement,
    InventoryMovementType,
)
from app.domains.inventory.repositories import (
    InMemoryInventoryMovementRepository,
)


def create_movement(
    code="MOV-001",
    movement_type=InventoryMovementType.ISSUE_TO_WORK_ORDER,
    spare_part_code="BRG-6206",
    quantity=2,
    source_location_code="LOC-001",
    target_location_code=None,
    quantity_before=10,
    quantity_after=8,
    work_order_code="WO-025",
    activity_code="WO-025-ACT-001",
    actor_person_code="TECH-001",
    occurred_at=None,
    observations="Consumo de refacción",
    transfer_code=None,
):

    if occurred_at is None:
        occurred_at = datetime(
            2026,
            9,
            15,
            10,
            0,
        )

    return InventoryMovement(
        code=code,
        movement_type=movement_type,
        spare_part_code=spare_part_code,
        quantity=quantity,
        source_location_code=source_location_code,
        target_location_code=target_location_code,
        quantity_before=quantity_before,
        quantity_after=quantity_after,
        work_order_code=work_order_code,
        activity_code=activity_code,
        actor_person_code=actor_person_code,
        occurred_at=occurred_at,
        observations=observations,
        transfer_code=transfer_code,
    )


def test_should_save_and_get_movement():

    repository = InMemoryInventoryMovementRepository()

    movement = create_movement()

    repository.save(movement)

    stored = repository.get_by_code("MOV-001")

    assert stored is movement


def test_get_by_code_should_normalize_code():

    repository = InMemoryInventoryMovementRepository()

    repository.save(create_movement())

    stored = repository.get_by_code(
        " mov-001 "
    )

    assert stored is not None
    assert stored.code == "MOV-001"


def test_get_unknown_movement_should_return_none():

    repository = InMemoryInventoryMovementRepository()

    assert repository.get_by_code("MOV-999") is None


def test_save_should_replace_same_movement_code():

    repository = InMemoryInventoryMovementRepository()

    repository.save(
        create_movement(
            observations="Anterior",
        )
    )

    repository.save(
        create_movement(
            observations="Actualizado",
        )
    )

    stored = repository.get_by_code("MOV-001")

    assert stored is not None
    assert stored.observations == "Actualizado"


def test_list_by_spare_part_should_filter_and_normalize():

    repository = InMemoryInventoryMovementRepository()

    repository.save(
        create_movement(
            code="MOV-001",
            spare_part_code="BRG-6206",
        )
    )

    repository.save(
        create_movement(
            code="MOV-002",
            spare_part_code="FUSE-001",
        )
    )

    movements = repository.list_by_spare_part(
        " brg-6206 "
    )

    assert [
        movement.code
        for movement in movements
    ] == ["MOV-001"]


def test_list_by_location_should_include_source_and_target():

    repository = InMemoryInventoryMovementRepository()

    repository.save(
        create_movement(
            code="MOV-001",
            source_location_code="LOC-001",
        )
    )

    repository.save(
        create_movement(
            code="MOV-002",
            movement_type=InventoryMovementType.RECEIPT,
            source_location_code=None,
            target_location_code="LOC-001",
            quantity=3,
            quantity_before=8,
            quantity_after=11,
            work_order_code=None,
            activity_code=None,
        )
    )

    repository.save(
        create_movement(
            code="MOV-003",
            source_location_code="LOC-002",
        )
    )

    movements = repository.list_by_location(
        " loc-001 "
    )

    assert {
        movement.code
        for movement in movements
    } == {
        "MOV-001",
        "MOV-002",
    }


def test_list_by_work_order_should_filter_and_normalize():

    repository = InMemoryInventoryMovementRepository()

    repository.save(
        create_movement(
            code="MOV-001",
            work_order_code="WO-025",
        )
    )

    repository.save(
        create_movement(
            code="MOV-002",
            work_order_code="WO-030",
        )
    )

    movements = repository.list_by_work_order(
        " wo-025 "
    )

    assert [
        movement.code
        for movement in movements
    ] == ["MOV-001"]


def test_list_by_transfer_code_should_return_both_legs():

    repository = InMemoryInventoryMovementRepository()

    repository.save(
        create_movement(
            code="MOV-001",
            movement_type=InventoryMovementType.TRANSFER_OUT,
            source_location_code="LOC-001",
            target_location_code=None,
            quantity=2,
            quantity_before=10,
            quantity_after=8,
            work_order_code=None,
            activity_code=None,
            transfer_code="TRF-001",
        )
    )

    repository.save(
        create_movement(
            code="MOV-002",
            movement_type=InventoryMovementType.TRANSFER_IN,
            source_location_code=None,
            target_location_code="LOC-002",
            quantity=2,
            quantity_before=3,
            quantity_after=5,
            work_order_code=None,
            activity_code=None,
            transfer_code="TRF-001",
        )
    )

    movements = repository.list_by_transfer_code(
        " trf-001 "
    )

    assert {
        movement.code
        for movement in movements
    } == {
        "MOV-001",
        "MOV-002",
    }


def test_queries_should_return_movements_in_chronological_order():

    repository = InMemoryInventoryMovementRepository()

    repository.save(
        create_movement(
            code="MOV-003",
            occurred_at=datetime(
                2026, 9, 15, 12, 0
            ),
        )
    )

    repository.save(
        create_movement(
            code="MOV-001",
            occurred_at=datetime(
                2026, 9, 15, 8, 0
            ),
        )
    )

    repository.save(
        create_movement(
            code="MOV-002",
            occurred_at=datetime(
                2026, 9, 15, 10, 0
            ),
        )
    )

    movements = repository.list_by_spare_part(
        "BRG-6206"
    )

    assert [
        movement.code
        for movement in movements
    ] == [
        "MOV-001",
        "MOV-002",
        "MOV-003",
    ]

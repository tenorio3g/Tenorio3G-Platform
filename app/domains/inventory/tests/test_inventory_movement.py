from datetime import datetime

import pytest

from app.domains.inventory.entities.inventory_movement import (
    InventoryMovement,
    InventoryMovementType,
)


OCCURRED_AT = datetime(
    2026,
    9,
    16,
    10,
    30,
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
    occurred_at=OCCURRED_AT,
    observations="Cambio de baleros",
    transfer_code=None,
):

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


def test_should_create_issue_to_work_order_movement():

    movement = create_movement()

    assert movement.code == "MOV-001"
    assert (
        movement.movement_type
        == InventoryMovementType.ISSUE_TO_WORK_ORDER
    )
    assert movement.spare_part_code == "BRG-6206"
    assert movement.quantity == 2
    assert movement.source_location_code == "LOC-001"
    assert movement.target_location_code is None
    assert movement.quantity_before == 10
    assert movement.quantity_after == 8
    assert movement.work_order_code == "WO-025"
    assert movement.activity_code == "WO-025-ACT-001"
    assert movement.actor_person_code == "TECH-001"
    assert movement.occurred_at == OCCURRED_AT
    assert movement.observations == "Cambio de baleros"


def test_should_normalize_codes():

    movement = create_movement(
        code=" mov-001 ",
        spare_part_code=" brg-6206 ",
        source_location_code=" loc-001 ",
        work_order_code=" wo-025 ",
        activity_code=" wo-025-act-001 ",
        actor_person_code=" tech-001 ",
    )

    assert movement.code == "MOV-001"
    assert movement.spare_part_code == "BRG-6206"
    assert movement.source_location_code == "LOC-001"
    assert movement.work_order_code == "WO-025"
    assert movement.activity_code == "WO-025-ACT-001"
    assert movement.actor_person_code == "TECH-001"


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("code", ""),
        ("code", "   "),
        ("spare_part_code", ""),
        ("spare_part_code", "   "),
        ("actor_person_code", ""),
        ("actor_person_code", "   "),
    ],
)
def test_should_reject_empty_required_codes(
    field_name,
    value,
):

    data = {
        "code": "MOV-001",
        "movement_type": (
            InventoryMovementType.ISSUE_TO_WORK_ORDER
        ),
        "spare_part_code": "BRG-6206",
        "quantity": 2,
        "source_location_code": "LOC-001",
        "quantity_before": 10,
        "quantity_after": 8,
        "work_order_code": "WO-025",
        "actor_person_code": "TECH-001",
        "occurred_at": OCCURRED_AT,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} is required",
    ):
        InventoryMovement(**data)


@pytest.mark.parametrize(
    "quantity",
    [
        0,
        -1,
    ],
)
def test_should_reject_non_positive_quantity(
    quantity,
):

    with pytest.raises(
        ValueError,
        match="quantity must be greater than zero",
    ):
        create_movement(
            quantity=quantity,
        )


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("quantity_before", -1),
        ("quantity_after", -1),
    ],
)
def test_should_reject_negative_stock_snapshots(
    field_name,
    value,
):

    data = {
        "quantity_before": 10,
        "quantity_after": 8,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} cannot be negative",
    ):
        create_movement(
            **data,
        )


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("quantity", float("nan")),
        ("quantity", float("inf")),
        ("quantity_before", float("nan")),
        ("quantity_after", float("inf")),
    ],
)
def test_should_reject_non_finite_numbers(
    field_name,
    value,
):

    data = {
        "quantity": 2,
        "quantity_before": 10,
        "quantity_after": 8,
    }

    data[field_name] = value

    with pytest.raises(
        ValueError,
        match=f"{field_name} must be finite",
    ):
        create_movement(
            **data,
        )


def test_should_reject_invalid_occurred_at():

    with pytest.raises(
        ValueError,
        match="occurred_at must be datetime",
    ):
        create_movement(
            occurred_at="2026-09-16",
        )


def test_receipt_should_require_target_location():

    with pytest.raises(
        ValueError,
        match="target_location_code is required for RECEIPT",
    ):
        create_movement(
            movement_type=InventoryMovementType.RECEIPT,
            source_location_code=None,
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
            quantity_before=0,
            quantity_after=2,
        )


def test_should_create_receipt():

    movement = create_movement(
        movement_type=InventoryMovementType.RECEIPT,
        source_location_code=None,
        target_location_code="LOC-001",
        work_order_code=None,
        activity_code=None,
        quantity_before=0,
        quantity_after=2,
    )

    assert movement.source_location_code is None
    assert movement.target_location_code == "LOC-001"


def test_issue_should_require_source_location():

    with pytest.raises(
        ValueError,
        match=(
            "source_location_code is required "
            "for ISSUE_TO_WORK_ORDER"
        ),
    ):
        create_movement(
            source_location_code=None,
        )


def test_issue_should_require_work_order():

    with pytest.raises(
        ValueError,
        match=(
            "work_order_code is required "
            "for ISSUE_TO_WORK_ORDER"
        ),
    ):
        create_movement(
            work_order_code=None,
            activity_code=None,
        )


def test_return_should_require_target_location():

    with pytest.raises(
        ValueError,
        match=(
            "target_location_code is required "
            "for RETURN_FROM_WORK_ORDER"
        ),
    ):
        create_movement(
            movement_type=(
                InventoryMovementType.RETURN_FROM_WORK_ORDER
            ),
            source_location_code=None,
            target_location_code=None,
            quantity_before=8,
            quantity_after=10,
        )


def test_return_should_require_work_order():

    with pytest.raises(
        ValueError,
        match=(
            "work_order_code is required "
            "for RETURN_FROM_WORK_ORDER"
        ),
    ):
        create_movement(
            movement_type=(
                InventoryMovementType.RETURN_FROM_WORK_ORDER
            ),
            source_location_code=None,
            target_location_code="LOC-001",
            work_order_code=None,
            activity_code=None,
            quantity_before=8,
            quantity_after=10,
        )


def test_should_create_transfer_out():

    movement = create_movement(
        movement_type=InventoryMovementType.TRANSFER_OUT,
        source_location_code="LOC-001",
        target_location_code=None,
        work_order_code=None,
        activity_code=None,
        quantity_before=10,
        quantity_after=8,
        transfer_code="TRF-001",
    )

    assert (
        movement.movement_type
        == InventoryMovementType.TRANSFER_OUT
    )
    assert movement.source_location_code == "LOC-001"
    assert movement.target_location_code is None


def test_transfer_out_should_require_source_location():

    with pytest.raises(
        ValueError,
        match=(
            "source_location_code is required "
            "for TRANSFER_OUT"
        ),
    ):
        create_movement(
            movement_type=InventoryMovementType.TRANSFER_OUT,
            source_location_code=None,
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
        )


def test_should_create_transfer_in():

    movement = create_movement(
        movement_type=InventoryMovementType.TRANSFER_IN,
        source_location_code=None,
        target_location_code="LOC-002",
        work_order_code=None,
        activity_code=None,
        quantity_before=3,
        quantity_after=5,
        transfer_code="TRF-001",
    )

    assert (
        movement.movement_type
        == InventoryMovementType.TRANSFER_IN
    )
    assert movement.source_location_code is None
    assert movement.target_location_code == "LOC-002"


def test_transfer_in_should_require_target_location():

    with pytest.raises(
        ValueError,
        match=(
            "target_location_code is required "
            "for TRANSFER_IN"
        ),
    ):
        create_movement(
            movement_type=InventoryMovementType.TRANSFER_IN,
            source_location_code=None,
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
        )


def test_adjustment_in_should_require_observations():

    with pytest.raises(
        ValueError,
        match="observations is required for ADJUSTMENT_IN",
    ):
        create_movement(
            movement_type=InventoryMovementType.ADJUSTMENT_IN,
            source_location_code=None,
            target_location_code="LOC-001",
            work_order_code=None,
            activity_code=None,
            quantity_before=8,
            quantity_after=10,
            observations="",
        )


def test_adjustment_in_should_require_target_location():

    with pytest.raises(
        ValueError,
        match=(
            "target_location_code is required "
            "for ADJUSTMENT_IN"
        ),
    ):
        create_movement(
            movement_type=InventoryMovementType.ADJUSTMENT_IN,
            source_location_code=None,
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
            quantity_before=8,
            quantity_after=10,
            observations="Conteo físico",
        )


def test_should_create_adjustment_in():

    movement = create_movement(
        movement_type=InventoryMovementType.ADJUSTMENT_IN,
        source_location_code=None,
        target_location_code="LOC-001",
        work_order_code=None,
        activity_code=None,
        quantity_before=8,
        quantity_after=10,
        observations=" Conteo físico ",
    )

    assert movement.target_location_code == "LOC-001"
    assert movement.observations == "Conteo físico"


def test_adjustment_out_should_require_observations():

    with pytest.raises(
        ValueError,
        match="observations is required for ADJUSTMENT_OUT",
    ):
        create_movement(
            movement_type=InventoryMovementType.ADJUSTMENT_OUT,
            source_location_code="LOC-001",
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
            quantity_before=10,
            quantity_after=8,
            observations="   ",
        )


def test_adjustment_out_should_require_source_location():

    with pytest.raises(
        ValueError,
        match=(
            "source_location_code is required "
            "for ADJUSTMENT_OUT"
        ),
    ):
        create_movement(
            movement_type=InventoryMovementType.ADJUSTMENT_OUT,
            source_location_code=None,
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
            quantity_before=10,
            quantity_after=8,
            observations="Diferencia en conteo físico",
        )


def test_should_create_adjustment_out():

    movement = create_movement(
        movement_type=InventoryMovementType.ADJUSTMENT_OUT,
        source_location_code="LOC-001",
        target_location_code=None,
        work_order_code=None,
        activity_code=None,
        quantity_before=10,
        quantity_after=8,
        observations="Diferencia en conteo físico",
    )

    assert movement.source_location_code == "LOC-001"
    assert movement.observations == (
        "Diferencia en conteo físico"
    )


def test_transfer_out_should_require_transfer_code():

    with pytest.raises(
        ValueError,
        match="transfer_code is required for TRANSFER_OUT",
    ):
        create_movement(
            movement_type=InventoryMovementType.TRANSFER_OUT,
            source_location_code="LOC-001",
            target_location_code=None,
            work_order_code=None,
            activity_code=None,
            quantity_before=10,
            quantity_after=8,
            transfer_code=None,
        )


def test_transfer_in_should_require_transfer_code():

    with pytest.raises(
        ValueError,
        match="transfer_code is required for TRANSFER_IN",
    ):
        create_movement(
            movement_type=InventoryMovementType.TRANSFER_IN,
            source_location_code=None,
            target_location_code="LOC-002",
            work_order_code=None,
            activity_code=None,
            quantity_before=3,
            quantity_after=5,
            transfer_code=None,
        )


def test_should_normalize_transfer_code():

    movement = create_movement(
        movement_type=InventoryMovementType.TRANSFER_OUT,
        source_location_code="LOC-001",
        target_location_code=None,
        work_order_code=None,
        activity_code=None,
        quantity_before=10,
        quantity_after=8,
        transfer_code=" trf-001 ",
    )

    assert movement.transfer_code == "TRF-001"


def test_non_transfer_should_allow_empty_transfer_code():

    movement = create_movement(
        transfer_code=None,
    )

    assert movement.transfer_code is None


@pytest.mark.parametrize(
    "movement_type",
    [
        InventoryMovementType.RECEIPT,
        InventoryMovementType.RETURN_FROM_WORK_ORDER,
        InventoryMovementType.ADJUSTMENT_IN,
        InventoryMovementType.TRANSFER_IN,
    ],
)
def test_should_reject_inconsistent_incoming_balance(
    movement_type,
):

    kwargs = {
        "movement_type": movement_type,
        "source_location_code": None,
        "target_location_code": "LOC-001",
        "quantity": 2,
        "quantity_before": 8,
        "quantity_after": 9,
        "work_order_code": None,
        "activity_code": None,
        "observations": "Conteo físico",
    }

    if (
        movement_type
        == InventoryMovementType.RETURN_FROM_WORK_ORDER
    ):
        kwargs["work_order_code"] = "WO-025"

    if (
        movement_type
        == InventoryMovementType.TRANSFER_IN
    ):
        kwargs["transfer_code"] = "TRF-001"

    with pytest.raises(
        ValueError,
        match="quantity_after is inconsistent with movement",
    ):
        create_movement(
            **kwargs,
        )


@pytest.mark.parametrize(
    "movement_type",
    [
        InventoryMovementType.ISSUE_TO_WORK_ORDER,
        InventoryMovementType.ADJUSTMENT_OUT,
        InventoryMovementType.TRANSFER_OUT,
    ],
)
def test_should_reject_inconsistent_outgoing_balance(
    movement_type,
):

    kwargs = {
        "movement_type": movement_type,
        "source_location_code": "LOC-001",
        "target_location_code": None,
        "quantity": 2,
        "quantity_before": 10,
        "quantity_after": 9,
        "work_order_code": None,
        "activity_code": None,
        "observations": "Conteo físico",
    }

    if (
        movement_type
        == InventoryMovementType.ISSUE_TO_WORK_ORDER
    ):
        kwargs["work_order_code"] = "WO-025"

    if (
        movement_type
        == InventoryMovementType.TRANSFER_OUT
    ):
        kwargs["transfer_code"] = "TRF-001"

    with pytest.raises(
        ValueError,
        match="quantity_after is inconsistent with movement",
    ):
        create_movement(
            **kwargs,
        )


def test_should_accept_consistent_receipt_balance():

    movement = create_movement(
        movement_type=InventoryMovementType.RECEIPT,
        source_location_code=None,
        target_location_code="LOC-001",
        quantity=5,
        quantity_before=10,
        quantity_after=15,
        work_order_code=None,
        activity_code=None,
    )

    assert movement.quantity_after == 15


def test_should_accept_consistent_issue_balance():

    movement = create_movement(
        quantity=2,
        quantity_before=10,
        quantity_after=8,
    )

    assert movement.quantity_after == 8


def test_should_accept_consistent_transfer_out_balance():

    movement = create_movement(
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

    assert movement.quantity_after == 8


def test_should_accept_consistent_transfer_in_balance():

    movement = create_movement(
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

    assert movement.quantity_after == 5


def test_outgoing_movement_should_reject_insufficient_stock():

    with pytest.raises(ValueError):
        create_movement(
            movement_type=(
                InventoryMovementType.ISSUE_TO_WORK_ORDER
            ),
            source_location_code="LOC-001",
            target_location_code=None,
            quantity=6,
            quantity_before=5,
            quantity_after=-1,
            work_order_code="WO-025",
            activity_code=None,
        )

from types import SimpleNamespace

from app.work_orders.work_order_queue import (
    filter_items_by_scope,
)


def create_item(
    code: str,
    technician_codes: list[str],
):
    return SimpleNamespace(
        code=code,
        technician_codes=technician_codes,
    )


def test_mine_scope_should_keep_only_orders_for_current_person():

    items = [
        create_item(
            "WO-001",
            ["TECH-001"],
        ),
        create_item(
            "WO-002",
            ["TECH-002"],
        ),
        create_item(
            "WO-003",
            ["TECH-001", "TECH-003"],
        ),
    ]

    filtered = filter_items_by_scope(
        items=items,
        scope="MINE",
        person_code="TECH-001",
    )

    assert [
        item.code
        for item in filtered
    ] == [
        "WO-001",
        "WO-003",
    ]

def test_all_scope_should_keep_all_orders():

    items = [
        create_item(
            "WO-001",
            ["TECH-001"],
        ),
        create_item(
            "WO-002",
            ["TECH-002"],
        ),
    ]

    filtered = filter_items_by_scope(
        items=items,
        scope="ALL",
        person_code="TECH-001",
    )

    assert [
        item.code
        for item in filtered
    ] == [
        "WO-001",
        "WO-002",
    ]


def test_mine_scope_without_person_should_return_empty_list():

    items = [
        create_item(
            "WO-001",
            ["TECH-001"],
        ),
    ]

    filtered = filter_items_by_scope(
        items=items,
        scope="MINE",
        person_code=None,
    )

    assert filtered == []


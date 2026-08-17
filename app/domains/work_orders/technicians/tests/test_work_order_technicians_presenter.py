from datetime import datetime

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.work_orders.technicians.entities import (
    WorkOrderTechnicianAssignment,
)

from app.domains.work_orders.technicians.presentation import (
    WorkOrderTechniciansPresenter,
)

from app.domains.work_orders.technicians.use_cases import (
    ListWorkOrderTechniciansResult,
    WorkOrderTechnicianItem,
)


def create_item(
    person_code,
    name,
    position="",
):

    return WorkOrderTechnicianItem(
        assignment=WorkOrderTechnicianAssignment(
            work_order_code="WO-001",
            person_code=person_code,
            assigned_at=datetime(
                2026,
                8,
                16,
                0,
                15,
            ),
        ),
        person=Person(
            code=person_code,
            name=name,
            position=position,
        ),
    )


def test_should_present_work_order_technicians():

    result = ListWorkOrderTechniciansResult(
        items=[
            create_item(
                "55464",
                "Fortunato",
                "Técnico",
            )
        ]
    )

    view_model = (
        WorkOrderTechniciansPresenter.present(
            result
        )
    )

    assert view_model.total == 1
    assert view_model.has_items is True

    item = view_model.items[0]

    assert item.person_code == "55464"
    assert item.name == "Fortunato"
    assert item.position == "Técnico"

    assert (
        item.assigned_at
        == "16/08/2026 00:15"
    )


def test_should_use_default_position():

    result = ListWorkOrderTechniciansResult(
        items=[
            create_item(
                "55464",
                "Fortunato",
            )
        ]
    )

    view_model = (
        WorkOrderTechniciansPresenter.present(
            result
        )
    )

    assert (
        view_model.items[0].position
        == "Sin puesto registrado"
    )


def test_should_order_technicians_by_name():

    result = ListWorkOrderTechniciansResult(
        items=[
            create_item(
                "002",
                "Pedro",
            ),
            create_item(
                "001",
                "Angel",
            ),
        ]
    )

    view_model = (
        WorkOrderTechniciansPresenter.present(
            result
        )
    )

    assert [
        item.name
        for item in view_model.items
    ] == [
        "Angel",
        "Pedro",
    ]


def test_should_present_empty_result():

    result = ListWorkOrderTechniciansResult(
        items=[]
    )

    view_model = (
        WorkOrderTechniciansPresenter.present(
            result
        )
    )

    assert view_model.items == []
    assert view_model.total == 0
    assert view_model.has_items is False
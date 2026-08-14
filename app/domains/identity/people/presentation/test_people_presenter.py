from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.presentation import (
    PeoplePresenter,
)


def test_should_present_people():

    people = [
        Person(
            code="TECH-001",
            name="Angel",
            position="Technician",
        )
    ]

    view_model = PeoplePresenter.present(
        people
    )

    assert view_model.has_items is True
    assert view_model.total == 1

    item = view_model.items[0]

    assert item.code == "TECH-001"
    assert item.name == "Angel"
    assert item.position == "Technician"
    assert item.status == "Activo"


def test_should_present_inactive_person():

    person = Person(
        code="TECH-001",
        name="Angel",
    )

    person.deactivate()

    view_model = PeoplePresenter.present(
        [person]
    )

    assert (
        view_model.items[0].status
        == "Inactivo"
    )


def test_should_use_default_position():

    person = Person(
        code="TECH-001",
        name="Angel",
        position="",
    )

    view_model = PeoplePresenter.present(
        [person]
    )

    assert (
        view_model.items[0].position
        == "Sin puesto registrado"
    )


def test_should_order_people_by_name():

    people = [
        Person(
            code="TECH-002",
            name="Daniel",
        ),
        Person(
            code="TECH-001",
            name="Angel",
        ),
    ]

    view_model = PeoplePresenter.present(
        people
    )

    assert [
        item.name
        for item in view_model.items
    ] == [
        "Angel",
        "Daniel",
    ]


def test_should_present_empty_list():

    view_model = PeoplePresenter.present(
        []
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.items == []
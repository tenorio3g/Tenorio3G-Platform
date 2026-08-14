from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.presentation import (
    UsersPresenter,
)


def create_user(
    username="angel",
    person_code="TECH-001",
    role_code="TECHNICIAN",
    is_active=True,
):
    return User(
        username=username,
        password_hash="HASH",
        person_code=person_code,
        role_code=role_code,
        is_active=is_active,
    )


def test_should_present_user():

    users = [
        create_user()
    ]

    people = [
        Person(
            code="TECH-001",
            name="Angel",
        )
    ]

    roles = [
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    ]

    view_model = UsersPresenter.present(
        users,
        people,
        roles,
    )

    assert view_model.has_items is True
    assert view_model.total == 1

    item = view_model.items[0]

    assert item.username == "angel"
    assert item.person_code == "TECH-001"
    assert item.person_name == "Angel"
    assert item.role_code == "TECHNICIAN"
    assert item.role_name == "Técnico"
    assert item.status == "Activo"
    assert item.is_active is True


def test_should_present_inactive_user():

    user = create_user(
        is_active=False
    )

    view_model = UsersPresenter.present(
        [user],
        [],
        [],
    )

    assert (
        view_model.items[0].status
        == "Inactivo"
    )

    assert (
        view_model.items[0].is_active
        is False
    )


def test_should_handle_missing_person():

    user = create_user()

    roles = [
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    ]

    view_model = UsersPresenter.present(
        [user],
        [],
        roles,
    )

    assert (
        view_model.items[0].person_name
        == "Persona no encontrada"
    )


def test_should_handle_missing_role():

    user = create_user()

    people = [
        Person(
            code="TECH-001",
            name="Angel",
        )
    ]

    view_model = UsersPresenter.present(
        [user],
        people,
        [],
    )

    assert (
        view_model.items[0].role_name
        == "Rol no encontrado"
    )


def test_should_order_users_by_username():

    users = [
        create_user(
            username="nato",
        ),
        create_user(
            username="angel",
        ),
        create_user(
            username="daniel",
        ),
    ]

    view_model = UsersPresenter.present(
        users,
        [],
        [],
    )

    assert [
        item.username
        for item in view_model.items
    ] == [
        "angel",
        "daniel",
        "nato",
    ]


def test_should_present_empty_list():

    view_model = UsersPresenter.present(
        [],
        [],
        [],
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.items == []
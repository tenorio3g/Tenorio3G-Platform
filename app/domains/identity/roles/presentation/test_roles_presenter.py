from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.presentation import (
    RolesPresenter,
)


def test_should_present_roles():

    roles = [
        Role(
            code="TECHNICIAN",
            name="Técnico",
            description="Personal técnico",
        )
    ]

    view_model = RolesPresenter.present(
        roles
    )

    assert view_model.has_items is True
    assert view_model.total == 1

    item = view_model.items[0]

    assert item.code == "TECHNICIAN"
    assert item.name == "Técnico"
    assert item.description == "Personal técnico"
    assert item.status == "Activo"
    assert item.is_active is True


def test_should_present_inactive_role():

    role = Role(
        code="TECHNICIAN",
        name="Técnico",
    )

    role.deactivate()

    view_model = RolesPresenter.present(
        [role]
    )

    assert view_model.items[0].status == "Inactivo"
    assert view_model.items[0].is_active is False


def test_should_use_default_description():

    role = Role(
        code="TECHNICIAN",
        name="Técnico",
        description="",
    )

    view_model = RolesPresenter.present(
        [role]
    )

    assert (
        view_model.items[0].description
        == "Sin descripción registrada"
    )


def test_should_order_roles_by_name():

    roles = [
        Role(
            code="TECHNICIAN",
            name="Técnico",
        ),
        Role(
            code="ADMIN",
            name="Administrador",
        ),
        Role(
            code="SUPERVISOR",
            name="Supervisor",
        ),
    ]

    view_model = RolesPresenter.present(
        roles
    )

    assert [
        item.name
        for item in view_model.items
    ] == [
        "Administrador",
        "Supervisor",
        "Técnico",
    ]


def test_should_present_empty_list():

    view_model = RolesPresenter.present(
        []
    )

    assert view_model.has_items is False
    assert view_model.total == 0
    assert view_model.items == []
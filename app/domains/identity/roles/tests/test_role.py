import pytest

from app.domains.identity.roles.entities import (
    Role,
)


def test_role_should_be_created():

    role = Role(
        code="TECHNICIAN",
        name="Técnico",
        description=(
            "Personal técnico de mantenimiento"
        ),
    )

    assert role.code == "TECHNICIAN"
    assert role.name == "Técnico"
    assert (
        role.description
        == "Personal técnico de mantenimiento"
    )
    assert role.is_active is True


def test_role_should_clean_values():

    role = Role(
        code="  technician  ",
        name="  Técnico  ",
        description="  Personal técnico  ",
    )

    assert role.code == "TECHNICIAN"
    assert role.name == "Técnico"
    assert (
        role.description
        == "Personal técnico"
    )


def test_role_should_require_code():

    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        Role(
            code="   ",
            name="Técnico",
        )


def test_role_should_require_name():

    with pytest.raises(
        ValueError,
        match="name is required",
    ):
        Role(
            code="TECHNICIAN",
            name="   ",
        )


def test_role_should_use_empty_description():

    role = Role(
        code="TECHNICIAN",
        name="Técnico",
        description=None,
    )

    assert role.description == ""


def test_role_should_be_deactivated_and_activated():

    role = Role(
        code="TECHNICIAN",
        name="Técnico",
    )

    role.deactivate()

    assert role.is_active is False

    role.activate()

    assert role.is_active is True
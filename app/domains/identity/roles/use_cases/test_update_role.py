import pytest

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)

from app.domains.identity.roles.use_cases import (
    UpdateRole,
    UpdateRoleCommand,
)


def test_should_update_role():

    repository = InMemoryRoleRepository()

    repository.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
            description="Rol técnico",
        )
    )

    use_case = UpdateRole(
        repository
    )

    result = use_case.execute(
        UpdateRoleCommand(
            code="TECHNICIAN",
            name="Técnico Senior",
            description="Rol técnico actualizado",
            is_active=False,
        )
    )

    assert result.role.code == "TECHNICIAN"
    assert result.role.name == "Técnico Senior"
    assert (
        result.role.description
        == "Rol técnico actualizado"
    )
    assert result.role.is_active is False

    persisted = repository.get_by_code(
        "TECHNICIAN"
    )

    assert persisted is not None
    assert persisted.name == "Técnico Senior"
    assert persisted.is_active is False


def test_should_reject_unknown_role():

    repository = InMemoryRoleRepository()

    use_case = UpdateRole(
        repository
    )

    with pytest.raises(
        ValueError,
        match="role not found",
    ):
        use_case.execute(
            UpdateRoleCommand(
                code="UNKNOWN",
                name="Unknown",
            )
        )
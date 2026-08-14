import pytest

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)

from app.domains.identity.roles.use_cases import (
    CreateRole,
    CreateRoleCommand,
)


def test_should_create_role():

    repository = InMemoryRoleRepository()

    use_case = CreateRole(
        repository
    )

    result = use_case.execute(
        CreateRoleCommand(
            code="TECHNICIAN",
            name="Técnico",
            description=(
                "Personal técnico"
            ),
        )
    )

    assert result.role.code == "TECHNICIAN"
    assert result.role.name == "Técnico"

    persisted = repository.get_by_code(
        "TECHNICIAN"
    )

    assert persisted is not None


def test_should_normalize_role_code():

    repository = InMemoryRoleRepository()

    use_case = CreateRole(
        repository
    )

    result = use_case.execute(
        CreateRoleCommand(
            code=" technician ",
            name="Técnico",
        )
    )

    assert result.role.code == "TECHNICIAN"


def test_should_reject_duplicate_role():

    repository = InMemoryRoleRepository()

    use_case = CreateRole(
        repository
    )

    use_case.execute(
        CreateRoleCommand(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    with pytest.raises(
        ValueError,
        match="role already exists",
    ):
        use_case.execute(
            CreateRoleCommand(
                code=" technician ",
                name="Otro técnico",
            )
        )
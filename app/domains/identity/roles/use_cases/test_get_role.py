from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)

from app.domains.identity.roles.use_cases import (
    GetRole,
    GetRoleQuery,
)


def test_should_get_role():

    repository = InMemoryRoleRepository()

    repository.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    use_case = GetRole(
        repository
    )

    result = use_case.execute(
        GetRoleQuery(
            code="TECHNICIAN",
        )
    )

    assert result.role is not None
    assert result.role.code == "TECHNICIAN"
    assert result.role.name == "Técnico"


def test_should_return_none_when_role_does_not_exist():

    repository = InMemoryRoleRepository()

    use_case = GetRole(
        repository
    )

    result = use_case.execute(
        GetRoleQuery(
            code="UNKNOWN",
        )
    )

    assert result.role is None
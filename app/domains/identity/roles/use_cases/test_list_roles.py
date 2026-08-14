from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)

from app.domains.identity.roles.use_cases import (
    ListRoles,
)


def test_should_list_roles():

    repository = InMemoryRoleRepository()

    repository.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    repository.save(
        Role(
            code="SUPERVISOR",
            name="Supervisor",
        )
    )

    use_case = ListRoles(
        repository
    )

    result = use_case.execute()

    assert len(result.roles) == 2

    assert {
        role.code
        for role in result.roles
    } == {
        "TECHNICIAN",
        "SUPERVISOR",
    }


def test_should_return_empty_list():

    repository = InMemoryRoleRepository()

    use_case = ListRoles(
        repository
    )

    result = use_case.execute()

    assert result.roles == []
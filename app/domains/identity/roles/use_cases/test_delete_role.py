from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)

from app.domains.identity.roles.use_cases import (
    DeleteRole,
    DeleteRoleCommand,
)


def test_should_delete_role():

    repository = InMemoryRoleRepository()

    repository.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    use_case = DeleteRole(
        repository
    )

    result = use_case.execute(
        DeleteRoleCommand(
            code="TECHNICIAN"
        )
    )

    assert result.deleted is True

    assert repository.get_by_code(
        "TECHNICIAN"
    ) is None


def test_should_return_false_when_role_does_not_exist():

    repository = InMemoryRoleRepository()

    use_case = DeleteRole(
        repository
    )

    result = use_case.execute(
        DeleteRoleCommand(
            code="UNKNOWN"
        )
    )

    assert result.deleted is False
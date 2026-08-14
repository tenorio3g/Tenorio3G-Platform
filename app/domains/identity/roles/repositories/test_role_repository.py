from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)


def create_role(
    code: str = "TECHNICIAN",
    name: str = "Técnico",
) -> Role:

    return Role(
        code=code,
        name=name,
        description="Rol de prueba",
    )


def test_should_save_and_get_role() -> None:

    repository = InMemoryRoleRepository()

    role = create_role()

    repository.save(role)

    persisted = repository.get_by_code(
        "TECHNICIAN"
    )

    assert persisted is not None
    assert persisted.code == "TECHNICIAN"
    assert persisted.name == "Técnico"


def test_should_get_role_with_normalized_code() -> None:

    repository = InMemoryRoleRepository()

    repository.save(
        create_role()
    )

    persisted = repository.get_by_code(
        " technician "
    )

    assert persisted is not None
    assert persisted.code == "TECHNICIAN"


def test_should_return_none_when_role_does_not_exist() -> None:

    repository = InMemoryRoleRepository()

    result = repository.get_by_code(
        "UNKNOWN"
    )

    assert result is None


def test_should_list_all_roles() -> None:

    repository = InMemoryRoleRepository()

    repository.save(
        create_role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    repository.save(
        create_role(
            code="SUPERVISOR",
            name="Supervisor",
        )
    )

    roles = repository.list_all()

    assert len(roles) == 2

    assert {
        role.code
        for role in roles
    } == {
        "TECHNICIAN",
        "SUPERVISOR",
    }


def test_should_update_existing_role() -> None:

    repository = InMemoryRoleRepository()

    role = create_role()

    repository.save(role)

    role.name = "Técnico Senior"

    repository.save(role)

    persisted = repository.get_by_code(
        "TECHNICIAN"
    )

    assert persisted is not None
    assert (
        persisted.name
        == "Técnico Senior"
    )

    assert len(
        repository.list_all()
    ) == 1


def test_should_delete_role() -> None:

    repository = InMemoryRoleRepository()

    repository.save(
        create_role()
    )

    deleted = repository.delete(
        " technician "
    )

    assert deleted is True

    assert repository.get_by_code(
        "TECHNICIAN"
    ) is None


def test_delete_should_return_false_when_role_does_not_exist() -> None:

    repository = InMemoryRoleRepository()

    deleted = repository.delete(
        "UNKNOWN"
    )

    assert deleted is False
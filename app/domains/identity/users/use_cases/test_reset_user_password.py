from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.use_cases.reset_user_password import (
    ResetUserPassword,
    ResetUserPasswordCommand,
)


def create_use_case():
    repository = InMemoryUserRepository()

    repository.save(
        User(
            username="supervisor.demo",
            password_hash="HASH-ANTERIOR",
            person_code="DEMO-SUP-001",
            role_code="SUPERVISOR",
            is_active=True,
        )
    )

    return (
        ResetUserPassword(repository),
        repository,
    )


def test_should_reset_user_password():
    use_case, repository = create_use_case()

    result = use_case.execute(
        ResetUserPasswordCommand(
            username="supervisor.demo",
            password_hash="HASH-NUEVO",
        )
    )

    persisted = repository.get_by_username(
        "supervisor.demo"
    )

    assert result.success is True
    assert persisted is not None
    assert persisted.password_hash == "HASH-NUEVO"

    assert (
        persisted.person_code
        == "DEMO-SUP-001"
    )
    assert (
        persisted.role_code
        == "SUPERVISOR"
    )
    assert persisted.is_active is True


def test_should_fail_when_user_does_not_exist():
    use_case, repository = create_use_case()

    result = use_case.execute(
        ResetUserPasswordCommand(
            username="missing.user",
            password_hash="HASH-NUEVO",
        )
    )

    assert result.success is False

    assert (
        repository.get_by_username(
            "missing.user"
        )
        is None
    )

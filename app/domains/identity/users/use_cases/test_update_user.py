import pytest

from app.domains.identity.people.entities import (
    Person,
)

from app.domains.identity.people.repositories import (
    InMemoryPersonRepository,
)

from app.domains.identity.roles.entities import (
    Role,
)

from app.domains.identity.roles.repositories import (
    InMemoryRoleRepository,
)

from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.use_cases import (
    UpdateUser,
    UpdateUserCommand,
)


def create_use_case():

    user_repository = (
        InMemoryUserRepository()
    )

    person_repository = (
        InMemoryPersonRepository()
    )

    role_repository = (
        InMemoryRoleRepository()
    )

    person_repository.save(
        Person(
            code="TECH-001",
            name="Angel",
        )
    )

    person_repository.save(
        Person(
            code="TECH-002",
            name="Daniel",
        )
    )

    role_repository.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    role_repository.save(
        Role(
            code="SUPERVISOR",
            name="Supervisor",
        )
    )

    user_repository.save(
        User(
            username="angel",
            password_hash="HASH-OLD",
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    use_case = UpdateUser(
        user_repository,
        person_repository,
        role_repository,
    )

    return (
        use_case,
        user_repository,
        person_repository,
        role_repository,
    )


def test_should_update_user():

    (
        use_case,
        user_repository,
        _,
        _,
    ) = create_use_case()

    result = use_case.execute(
        UpdateUserCommand(
            username="angel",
            password_hash="HASH-NEW",
            person_code="TECH-002",
            role_code="SUPERVISOR",
            is_active=False,
        )
    )

    assert result.user.username == "angel"
    assert result.user.password_hash == "HASH-NEW"
    assert result.user.person_code == "TECH-002"
    assert result.user.role_code == "SUPERVISOR"
    assert result.user.is_active is False

    persisted = (
        user_repository
        .get_by_username(
            "angel"
        )
    )

    assert persisted is not None
    assert persisted.role_code == "SUPERVISOR"


def test_should_reject_unknown_user():

    (
        use_case,
        _,
        _,
        _,
    ) = create_use_case()

    with pytest.raises(
        ValueError,
        match="user not found",
    ):
        use_case.execute(
            UpdateUserCommand(
                username="unknown",
                password_hash="HASH",
                person_code="TECH-001",
                role_code="TECHNICIAN",
            )
        )


def test_should_reject_unknown_person():

    (
        use_case,
        _,
        _,
        _,
    ) = create_use_case()

    with pytest.raises(
        ValueError,
        match="person not found",
    ):
        use_case.execute(
            UpdateUserCommand(
                username="angel",
                password_hash="HASH",
                person_code="UNKNOWN",
                role_code="TECHNICIAN",
            )
        )


def test_should_reject_unknown_role():

    (
        use_case,
        _,
        _,
        _,
    ) = create_use_case()

    with pytest.raises(
        ValueError,
        match="role not found",
    ):
        use_case.execute(
            UpdateUserCommand(
                username="angel",
                password_hash="HASH",
                person_code="TECH-001",
                role_code="UNKNOWN",
            )
        )


def test_should_reject_inactive_person():

    (
        use_case,
        _,
        person_repository,
        _,
    ) = create_use_case()

    person = person_repository.get_by_code(
        "TECH-002"
    )

    assert person is not None

    person.deactivate()
    person_repository.save(person)

    with pytest.raises(
        ValueError,
        match="person is inactive",
    ):
        use_case.execute(
            UpdateUserCommand(
                username="angel",
                password_hash="HASH",
                person_code="TECH-002",
                role_code="TECHNICIAN",
            )
        )


def test_should_reject_inactive_role():

    (
        use_case,
        _,
        _,
        role_repository,
    ) = create_use_case()

    role = role_repository.get_by_code(
        "SUPERVISOR"
    )

    assert role is not None

    role.deactivate()
    role_repository.save(role)

    with pytest.raises(
        ValueError,
        match="role is inactive",
    ):
        use_case.execute(
            UpdateUserCommand(
                username="angel",
                password_hash="HASH",
                person_code="TECH-001",
                role_code="SUPERVISOR",
            )
        )
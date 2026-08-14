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

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.use_cases import (
    CreateUser,
    CreateUserCommand,
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

    role_repository.save(
        Role(
            code="TECHNICIAN",
            name="Técnico",
        )
    )

    use_case = CreateUser(
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


def test_should_create_user():

    (
        use_case,
        user_repository,
        _,
        _,
    ) = create_use_case()

    result = use_case.execute(
        CreateUserCommand(
            username="angel",
            password_hash="HASH",
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    assert result.user.username == "angel"
    assert result.user.person_code == "TECH-001"
    assert result.user.role_code == "TECHNICIAN"

    persisted = (
        user_repository
        .get_by_username(
            "angel"
        )
    )

    assert persisted is not None


def test_should_reject_duplicate_user():

    (
        use_case,
        _,
        _,
        _,
    ) = create_use_case()

    command = CreateUserCommand(
        username="angel",
        password_hash="HASH",
        person_code="TECH-001",
        role_code="TECHNICIAN",
    )

    use_case.execute(command)

    with pytest.raises(
        ValueError,
        match="user already exists",
    ):
        use_case.execute(command)


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
            CreateUserCommand(
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
            CreateUserCommand(
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

    person = (
        person_repository
        .get_by_code(
            "TECH-001"
        )
    )

    assert person is not None

    person.deactivate()

    person_repository.save(
        person
    )

    with pytest.raises(
        ValueError,
        match="person is inactive",
    ):
        use_case.execute(
            CreateUserCommand(
                username="angel",
                password_hash="HASH",
                person_code="TECH-001",
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

    role = (
        role_repository
        .get_by_code(
            "TECHNICIAN"
        )
    )

    assert role is not None

    role.deactivate()

    role_repository.save(
        role
    )

    with pytest.raises(
        ValueError,
        match="role is inactive",
    ):
        use_case.execute(
            CreateUserCommand(
                username="angel",
                password_hash="HASH",
                person_code="TECH-001",
                role_code="TECHNICIAN",
            )
        )
from app.domains.identity.users.entities import (
    User,
)

from app.domains.identity.users.repositories import (
    InMemoryUserRepository,
)

from app.domains.identity.users.security import (
    WerkzeugPasswordHasher,
)

from app.domains.identity.authentication.use_cases import (
    AuthenticateUser,
    AuthenticateUserCommand,
)


def create_authentication():

    repository = InMemoryUserRepository()

    password_hasher = (
        WerkzeugPasswordHasher()
    )

    password_hash = password_hasher.hash(
        "Secret123"
    )

    repository.save(
        User(
            username="angel",
            password_hash=password_hash,
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )
    )

    authenticate_user = AuthenticateUser(
        repository,
        password_hasher,
    )

    return (
        authenticate_user,
        repository,
    )


def test_should_authenticate_valid_user():

    authenticate_user, _ = (
        create_authentication()
    )

    result = authenticate_user.execute(
        AuthenticateUserCommand(
            username="angel",
            password="Secret123",
        )
    )

    assert result.authenticated is True

    assert result.user is not None
    assert result.user.username == "angel"
    assert result.user.role_code == "TECHNICIAN"


def test_should_normalize_username():

    authenticate_user, _ = (
        create_authentication()
    )

    result = authenticate_user.execute(
        AuthenticateUserCommand(
            username=" ANGEL ",
            password="Secret123",
        )
    )

    assert result.authenticated is True
    assert result.user is not None
    assert result.user.username == "angel"


def test_should_reject_wrong_password():

    authenticate_user, _ = (
        create_authentication()
    )

    result = authenticate_user.execute(
        AuthenticateUserCommand(
            username="angel",
            password="WrongPassword",
        )
    )

    assert result.authenticated is False
    assert result.user is None


def test_should_reject_unknown_user():

    authenticate_user, _ = (
        create_authentication()
    )

    result = authenticate_user.execute(
        AuthenticateUserCommand(
            username="unknown",
            password="Secret123",
        )
    )

    assert result.authenticated is False
    assert result.user is None


def test_should_reject_inactive_user():

    (
        authenticate_user,
        repository,
    ) = create_authentication()

    user = repository.get_by_username(
        "angel"
    )

    assert user is not None

    user.deactivate()

    repository.save(user)

    result = authenticate_user.execute(
        AuthenticateUserCommand(
            username="angel",
            password="Secret123",
        )
    )

    assert result.authenticated is False
    assert result.user is None


def test_should_reject_empty_password():

    authenticate_user, _ = (
        create_authentication()
    )

    result = authenticate_user.execute(
        AuthenticateUserCommand(
            username="angel",
            password="",
        )
    )

    assert result.authenticated is False
    assert result.user is None
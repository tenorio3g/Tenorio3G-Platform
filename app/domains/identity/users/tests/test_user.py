import pytest

from app.domains.identity.users.entities import (
    User,
)


def create_user() -> User:

    return User(
        username="angel",
        password_hash="HASH-DE-PRUEBA",
        person_code="TECH-001",
        role_code="TECHNICIAN",
    )


def test_user_should_be_created():

    user = create_user()

    assert user.username == "angel"
    assert (
        user.password_hash
        == "HASH-DE-PRUEBA"
    )
    assert user.person_code == "TECH-001"
    assert user.role_code == "TECHNICIAN"
    assert user.is_active is True


def test_user_should_normalize_values():

    user = User(
        username="  ANGEL  ",
        password_hash="  HASH-DE-PRUEBA  ",
        person_code="  tech-001  ",
        role_code="  technician  ",
    )

    assert user.username == "angel"
    assert (
        user.password_hash
        == "HASH-DE-PRUEBA"
    )
    assert user.person_code == "TECH-001"
    assert user.role_code == "TECHNICIAN"


def test_user_should_require_username():

    with pytest.raises(
        ValueError,
        match="username is required",
    ):
        User(
            username="   ",
            password_hash="HASH",
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )


def test_user_should_require_password_hash():

    with pytest.raises(
        ValueError,
        match="password_hash is required",
    ):
        User(
            username="angel",
            password_hash="   ",
            person_code="TECH-001",
            role_code="TECHNICIAN",
        )


def test_user_should_require_person_code():

    with pytest.raises(
        ValueError,
        match="person_code is required",
    ):
        User(
            username="angel",
            password_hash="HASH",
            person_code="   ",
            role_code="TECHNICIAN",
        )


def test_user_should_require_role_code():

    with pytest.raises(
        ValueError,
        match="role_code is required",
    ):
        User(
            username="angel",
            password_hash="HASH",
            person_code="TECH-001",
            role_code="   ",
        )


def test_user_should_be_deactivated_and_activated():

    user = create_user()

    user.deactivate()

    assert user.is_active is False

    user.activate()

    assert user.is_active is True
import pytest

from app.domains.identity.users.security import (
    WerkzeugPasswordHasher,
)


def test_should_hash_password():

    hasher = WerkzeugPasswordHasher()

    password_hash = hasher.hash(
        "Secret123"
    )

    assert password_hash
    assert password_hash != "Secret123"


def test_should_verify_correct_password():

    hasher = WerkzeugPasswordHasher()

    password_hash = hasher.hash(
        "Secret123"
    )

    assert hasher.verify(
        "Secret123",
        password_hash,
    ) is True


def test_should_reject_wrong_password():

    hasher = WerkzeugPasswordHasher()

    password_hash = hasher.hash(
        "Secret123"
    )

    assert hasher.verify(
        "WrongPassword",
        password_hash,
    ) is False


def test_should_generate_different_hashes_for_same_password():

    hasher = WerkzeugPasswordHasher()

    hash_one = hasher.hash(
        "Secret123"
    )

    hash_two = hasher.hash(
        "Secret123"
    )

    assert hash_one != hash_two

    assert hasher.verify(
        "Secret123",
        hash_one,
    ) is True

    assert hasher.verify(
        "Secret123",
        hash_two,
    ) is True


def test_should_reject_empty_password():

    hasher = WerkzeugPasswordHasher()

    with pytest.raises(
        ValueError,
        match="password is required",
    ):
        hasher.hash("")


def test_verify_should_return_false_for_empty_values():

    hasher = WerkzeugPasswordHasher()

    assert hasher.verify(
        "",
        "HASH",
    ) is False

    assert hasher.verify(
        "Secret123",
        "",
    ) is False
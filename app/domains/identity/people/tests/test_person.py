import pytest

from app.domains.identity.people.entities import (
    Person,
)


def test_person_should_be_created():
    person = Person(
        code="TECH-001",
        name="Angel",
        position="Technician",
    )

    assert person.code == "TECH-001"
    assert person.name == "Angel"
    assert person.position == "Technician"
    assert person.is_active is True


def test_person_should_clean_text_values():
    person = Person(
        code="  TECH-001  ",
        name="  Angel  ",
        position="  Technician  ",
    )

    assert person.code == "TECH-001"
    assert person.name == "Angel"
    assert person.position == "Technician"


def test_person_should_require_code():
    with pytest.raises(
        ValueError,
        match="code is required",
    ):
        Person(
            code="   ",
            name="Angel",
        )


def test_person_should_require_name():
    with pytest.raises(
        ValueError,
        match="name is required",
    ):
        Person(
            code="TECH-001",
            name="   ",
        )


def test_person_should_be_deactivated_and_activated():
    person = Person(
        code="TECH-001",
        name="Angel",
    )

    person.deactivate()

    assert person.is_active is False

    person.activate()

    assert person.is_active is True
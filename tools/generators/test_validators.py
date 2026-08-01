import pytest

from tools.generators.validators import (
    ModuleNameValidator,
)


@pytest.mark.parametrize(
    "module_name",
    [
        "Inventory",
        "Knowledge",
        "Assets",
        "WorkOrders",
        "People",
    ],
)
def test_should_accept_valid_module_names(
    module_name: str,
) -> None:

    ModuleNameValidator.validate(
        module_name
    )


@pytest.mark.parametrize(
    ("module_name", "expected_message"),
    [
        (
            "",
            "Module name cannot be empty.",
        ),
        (
            "Io",
            "Module name must contain at least 3 characters.",
        ),
        (
            "inventory",
            "Module name must start with an uppercase letter.",
        ),
        (
            "123Module",
            "Module name must start with an uppercase letter.",
        ),
        (
            "My Module",
            "Module name may contain only alphabetic characters.",
        ),
        (
            "My-Module",
            "Module name may contain only alphabetic characters.",
        ),
        (
            "Inventory123",
            "Module name may contain only alphabetic characters.",
        ),
    ],
)
def test_should_reject_invalid_module_names(
    module_name: str,
    expected_message: str,
) -> None:

    with pytest.raises(
        ValueError,
        match=expected_message,
    ):
        ModuleNameValidator.validate(
            module_name
        )


def test_should_reject_non_string_module_name() -> None:

    with pytest.raises(
        TypeError,
        match="Module name must be a string.",
    ):
        ModuleNameValidator.validate(
            123,  # type: ignore[arg-type]
        )
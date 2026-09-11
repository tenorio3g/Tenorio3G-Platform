from pathlib import Path


APP_PATH = Path("app/__init__.py")

TEMPLATE_PATH = Path(
    "app/templates/pages/errors/403.html"
)


def test_app_should_register_403_error_handler():
    source = APP_PATH.read_text(
        encoding="utf-8"
    )

    assert "register_error_handler" in source
    assert "403" in source


def test_403_template_should_exist():
    assert TEMPLATE_PATH.exists()


def test_403_template_should_extend_base_layout():
    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert 'extends "layouts/base.html"' in source


def test_403_template_should_explain_access_restriction():
    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert "Acceso restringido" in source
    assert "administrador" in source.lower()


def test_403_template_should_offer_navigation():
    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert "history.back()" in source
    assert "core.dashboard" in source

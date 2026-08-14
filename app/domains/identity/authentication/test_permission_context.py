from app import create_app

from app.domains.identity.authentication import (
    can,
)


def test_can_should_return_false_without_role():

    app = create_app()
    app.config["TESTING"] = True

    with app.test_request_context():

        assert can(
            "assets.view"
        ) is False


def test_admin_should_manage_documents():

    app = create_app()
    app.config["TESTING"] = True

    with app.test_request_context():

        from flask import session

        session["role_code"] = "ADMIN"

        assert can(
            "documents.manage"
        ) is True


def test_manager_should_not_manage_documents():

    app = create_app()
    app.config["TESTING"] = True

    with app.test_request_context():

        from flask import session

        session["role_code"] = "MANAGER"

        assert can(
            "documents.manage"
        ) is False


def test_technician_should_manage_maintenance():

    app = create_app()
    app.config["TESTING"] = True

    with app.test_request_context():

        from flask import session

        session["role_code"] = "TECHNICIAN"

        assert can(
            "maintenance.manage"
        ) is True


def test_can_should_be_available_in_jinja():

    app = create_app()
    app.config["TESTING"] = True

    with app.test_request_context():

        from flask import session

        session["role_code"] = "ADMIN"

        template = app.jinja_env.from_string(
            """
            {% if can("users.manage") %}
                ALLOWED
            {% else %}
                DENIED
            {% endif %}
            """
        )

        result = template.render()

        assert "ALLOWED" in result
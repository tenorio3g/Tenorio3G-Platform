from flask import Blueprint

from app import create_app

from app.domains.identity.authentication import (
    role_required,
)


def test_should_redirect_when_not_authenticated():

    app = create_app()
    app.config["TESTING"] = True

    client = app.test_client()

    response = client.get(
        "/usuarios",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )




def build_test_app():

    app = create_app()

    app.config["TESTING"] = True

    test_blueprint = Blueprint(
        "authorization_test",
        __name__,
    )

    @test_blueprint.route(
        "/authorization/admin"
    )
    @role_required(
        "ADMIN",
    )
    def admin_only():
        return "admin"

    @test_blueprint.route(
        "/authorization/management"
    )
    @role_required(
        "ADMIN",
        "SUPERVISOR",
    )
    def management():
        return "management"

    app.register_blueprint(
        test_blueprint
    )

    return app


def test_role_required_should_redirect_without_session():

    app = build_test_app()

    client = app.test_client()

    response = client.get(
        "/authorization/admin",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )


def test_role_required_should_allow_authorized_role():

    app = build_test_app()

    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/authorization/admin"
    )

    assert response.status_code == 200

    assert (
        response.get_data(
            as_text=True
        )
        == "admin"
    )


def test_role_required_should_reject_unauthorized_role():

    app = build_test_app()

    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/authorization/admin"
    )

    assert response.status_code == 403


def test_role_required_should_allow_multiple_roles():

    app = build_test_app()

    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        "/authorization/management"
    )

    assert response.status_code == 200


def test_role_required_should_normalize_session_role():

    app = build_test_app()

    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["role_code"] = " admin "

    response = client.get(
        "/authorization/admin"
    )

    assert response.status_code == 200


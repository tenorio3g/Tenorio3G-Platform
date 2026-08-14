from flask import Blueprint

from app import create_app

from app.domains.identity.authentication import (
    permission_required,
)


def build_test_app():

    app = create_app()

    app.config["TESTING"] = True

    test_blueprint = Blueprint(
        "permission_test",
        __name__,
    )

    @test_blueprint.route(
        "/permission/assets"
    )
    @permission_required(
        "assets.view"
    )
    def assets_view():
        return "assets"

    @test_blueprint.route(
        "/permission/users"
    )
    @permission_required(
        "users.manage"
    )
    def users_manage():
        return "users"

    @test_blueprint.route(
        "/permission/people"
    )
    @permission_required(
        "people.manage"
    )
    def people_manage():
        return "people"

    app.register_blueprint(
        test_blueprint
    )

    return app


def test_should_redirect_without_session():

    app = build_test_app()
    client = app.test_client()

    response = client.get(
        "/permission/assets",
        follow_redirects=False,
    )

    assert response.status_code == 302

    assert (
        "/login"
        in response.headers["Location"]
    )


def test_technician_should_view_assets():

    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/permission/assets"
    )

    assert response.status_code == 200


def test_technician_should_not_manage_users():

    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "angel"
        session["role_code"] = "TECHNICIAN"

    response = client.get(
        "/permission/users"
    )

    assert response.status_code == 403


def test_admin_should_manage_users():

    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "admin"
        session["role_code"] = "ADMIN"

    response = client.get(
        "/permission/users"
    )

    assert response.status_code == 200


def test_supervisor_should_manage_people():

    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "supervisor"
        session["role_code"] = "SUPERVISOR"

    response = client.get(
        "/permission/people"
    )

    assert response.status_code == 200


def test_manager_should_not_manage_people():

    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "manager"
        session["role_code"] = "MANAGER"

    response = client.get(
        "/permission/people"
    )

    assert response.status_code == 403


def test_unknown_role_should_be_forbidden():

    app = build_test_app()
    client = app.test_client()

    with client.session_transaction() as session:
        session["username"] = "unknown"
        session["role_code"] = "UNKNOWN"

    response = client.get(
        "/permission/assets"
    )

    assert response.status_code == 403
from pathlib import Path


ROUTES_PATH = Path(
    "app/identity/routes.py"
)


def test_password_reset_route_should_exist():
    source = ROUTES_PATH.read_text(
        encoding="utf-8"
    )

    assert (
        '"/usuarios/<string:username>/'
        'restablecer-contrasena"'
        in source
    )


def test_password_reset_route_should_accept_get_and_post():
    source = ROUTES_PATH.read_text(
        encoding="utf-8"
    )

    route_start = source.index(
        '"/usuarios/<string:username>/'
        'restablecer-contrasena"'
    )

    route_source = source[
        route_start:
        route_start + 300
    ]

    assert 'methods=["GET", "POST"]' in route_source


def test_password_reset_route_should_require_users_manage():
    source = ROUTES_PATH.read_text(
        encoding="utf-8"
    )

    route_start = source.index(
        '"/usuarios/<string:username>/'
        'restablecer-contrasena"'
    )

    route_source = source[
        route_start:
        route_start + 400
    ]

    assert (
        '@permission_required("users.manage")'
        in route_source
    )

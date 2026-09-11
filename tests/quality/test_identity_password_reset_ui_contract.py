from pathlib import Path


TEMPLATE_PATH = Path(
    "app/templates/pages/users/index.html"
)


def test_users_index_should_offer_password_reset_action():
    source = TEMPLATE_PATH.read_text(
        encoding="utf-8"
    )

    assert (
        "identity.reset_user_password_route"
        in source
    )

    assert (
        "Restablecer contrase?a"
        in source
    )

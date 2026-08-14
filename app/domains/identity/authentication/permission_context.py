from flask import session

from app.domains.identity.permissions import (
    PermissionPolicy,
)


def can(
    permission: str,
) -> bool:

    role_code = session.get(
        "role_code",
        "",
    )

    return PermissionPolicy.has_permission(
        role_code,
        permission,
    )
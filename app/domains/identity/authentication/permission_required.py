from functools import wraps

from flask import (
    abort,
    redirect,
    session,
    url_for,
)

from app.domains.identity.permissions import (
    PermissionPolicy,
)


def permission_required(
    permission: str,
):

    def decorator(
        view_function,
    ):

        @wraps(view_function)
        def wrapped_view(
            *args,
            **kwargs,
        ):

            username = session.get(
                "username"
            )

            if not username:

                return redirect(
                    url_for(
                        "identity.login_route"
                    )
                )

            role_code = session.get(
                "role_code",
                "",
            )

            if not PermissionPolicy.has_permission(
                role_code,
                permission,
            ):
                abort(403)

            return view_function(
                *args,
                **kwargs,
            )

        return wrapped_view

    return decorator
from functools import wraps

from flask import (
    abort,
    redirect,
    session,
    url_for,
)


def role_required(*allowed_roles):

    normalized_roles = {
        str(role).strip().upper()
        for role in allowed_roles
    }

    def decorator(view_function):

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

            role_code = str(
                session.get(
                    "role_code",
                    "",
                )
            ).strip().upper()

            if (
                role_code
                not in normalized_roles
            ):
                abort(403)

            return view_function(
                *args,
                **kwargs
            )

        return wrapped_view

    return decorator
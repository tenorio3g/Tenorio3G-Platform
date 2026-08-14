from functools import wraps

from flask import (
    redirect,
    session,
    url_for,
)


def login_required(view_function):

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):

        username = session.get(
            "username"
        )

        if not username:

            return redirect(
                url_for(
                    "identity.login_route"
                )
            )

        return view_function(
            *args,
            **kwargs
        )

    return wrapped_view
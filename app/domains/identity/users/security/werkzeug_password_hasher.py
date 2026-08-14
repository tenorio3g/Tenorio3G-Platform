from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from .password_hasher import (
    PasswordHasher,
)


class WerkzeugPasswordHasher(
    PasswordHasher
):

    def hash(
        self,
        password: str,
    ) -> str:

        password = str(password)

        if not password:
            raise ValueError(
                "password is required"
            )

        return generate_password_hash(
            password
        )

    def verify(
        self,
        password: str,
        password_hash: str,
    ) -> bool:

        if not password:
            return False

        if not password_hash:
            return False

        return check_password_hash(
            password_hash,
            password,
        )
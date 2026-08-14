from app.domains.identity.authentication.use_cases import (
    AuthenticateUser,
)

from app.domains.identity.users.bootstrap import (
    password_hasher,
    user_repository,
)


authenticate_user = AuthenticateUser(
    user_repository,
    password_hasher,
)
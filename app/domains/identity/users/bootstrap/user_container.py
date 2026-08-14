from app.foundation.database import (
    SessionLocal,
)

from app.domains.identity.people.bootstrap import (
    person_repository,
)

from app.domains.identity.roles.bootstrap import (
    role_repository,
)

from app.domains.identity.users.repositories import (
    SQLiteUserRepository,
)

from app.domains.identity.users.use_cases import (
    CreateUser,
    DeleteUser,
    GetUser,
    ListUsers,
    UpdateUser,
)

from app.domains.identity.users.security import (
    WerkzeugPasswordHasher,
)


user_repository = SQLiteUserRepository(
    SessionLocal
)

create_user = CreateUser(
    user_repository,
    person_repository,
    role_repository,
)

get_user = GetUser(
    user_repository
)

list_users = ListUsers(
    user_repository
)

update_user = UpdateUser(
    user_repository,
    person_repository,
    role_repository,
)

delete_user = DeleteUser(
    user_repository
)

password_hasher = WerkzeugPasswordHasher()
from app.foundation.database import SessionLocal

from app.domains.identity.roles.repositories import (
    SQLiteRoleRepository,
)

from app.domains.identity.roles.use_cases import (
    CreateRole,
    DeleteRole,
    GetRole,
    ListRoles,
    UpdateRole,
)


role_repository = SQLiteRoleRepository(
    SessionLocal
)

create_role = CreateRole(
    role_repository
)

get_role = GetRole(
    role_repository
)

list_roles = ListRoles(
    role_repository
)

update_role = UpdateRole(
    role_repository
)

delete_role = DeleteRole(
    role_repository
)
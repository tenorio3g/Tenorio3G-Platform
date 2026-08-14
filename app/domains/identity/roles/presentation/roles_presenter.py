from app.domains.identity.roles.entities import (
    Role,
)

from .roles_view_model import (
    RoleItemViewModel,
    RolesViewModel,
)


class RolesPresenter:

    @staticmethod
    def present(
        roles: list[Role],
    ) -> RolesViewModel:

        ordered_roles = sorted(
            roles,
            key=lambda role: role.name.lower(),
        )

        items = [
            RoleItemViewModel(
                code=role.code,
                name=role.name,
                description=(
                    role.description
                    or "Sin descripción registrada"
                ),
                status=(
                    "Activo"
                    if role.is_active
                    else "Inactivo"
                ),
                is_active=role.is_active,
            )
            for role in ordered_roles
        ]

        return RolesViewModel(
            items=items
        )
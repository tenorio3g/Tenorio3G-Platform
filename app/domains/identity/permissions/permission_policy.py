class PermissionPolicy:

    ROLE_PERMISSIONS = {
        "ADMIN": {
            "assets.view",

            "people.view",
            "people.manage",

            "roles.view",
            "roles.manage",

            "users.view",
            "users.manage",

            "documents.view",
            "documents.manage",

            "photos.view",
            "photos.manage",

            "maintenance.view",
            "maintenance.manage",
            "maintenance.view",
            "maintenance.manage",

            "preventive.view",
            "preventive.manage",
        },

        "MANAGER": {
            "assets.view",

            "people.view",

            "documents.view",

            "photos.view",

            "maintenance.view",
            "maintenance.view",
            "preventive.view",
        },

        "SUPERVISOR": {
            "assets.view",

            "people.view",
            "people.manage",

            "documents.view",
            "documents.manage",

            "photos.view",
            "photos.manage",

            "maintenance.view",
            "maintenance.manage",
            "maintenance.view",
            "maintenance.manage",

            "preventive.view",
            "preventive.manage",
        },

        "TECHNICIAN": {
            "assets.view",

            "documents.view",

            "photos.view",

            "maintenance.view",
            "maintenance.manage",
            "maintenance.view",
            "maintenance.manage",

            "preventive.view",
        },
    }

    @classmethod
    def has_permission(
        cls,
        role_code: str,
        permission: str,
    ) -> bool:

        normalized_role = str(
            role_code
        ).strip().upper()

        normalized_permission = str(
            permission
        ).strip().lower()

        permissions = cls.ROLE_PERMISSIONS.get(
            normalized_role,
            set(),
        )

        return (
            normalized_permission
            in permissions
        )

    @classmethod
    def permissions_for(
        cls,
        role_code: str,
    ) -> set[str]:

        normalized_role = str(
            role_code
        ).strip().upper()

        return set(
            cls.ROLE_PERMISSIONS.get(
                normalized_role,
                set(),
            )
        )
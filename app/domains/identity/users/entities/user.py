class User:

    def __init__(
        self,
        username,
        password_hash,
        person_code,
        role_code,
        is_active=True,
    ):
        self.username = self._clean_required(
            username,
            "username",
        ).lower()

        self.password_hash = self._clean_required(
            password_hash,
            "password_hash",
        )

        self.person_code = self._clean_required(
            person_code,
            "person_code",
        ).upper()

        self.role_code = self._clean_required(
            role_code,
            "role_code",
        ).upper()

        self.is_active = bool(
            is_active
        )

    @staticmethod
    def _clean_required(
        value,
        field_name,
    ):
        value = str(value).strip()

        if not value:
            raise ValueError(
                f"{field_name} is required"
            )

        return value

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
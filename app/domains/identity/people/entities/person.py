class Person:

    def __init__(
        self,
        code,
        name,
        position="",
        is_active=True,
    ):
        self.code = self._clean_required(
            code,
            "code",
        )
        self.name = self._clean_required(
            name,
            "name",
        )
        self.position = self._clean_optional(
            position,
        )
        self.is_active = bool(is_active)

    @staticmethod
    def _clean_required(value, field_name):
        value = str(value).strip()

        if not value:
            raise ValueError(
                f"{field_name} is required"
            )

        return value

    @staticmethod
    def _clean_optional(value):
        if value is None:
            return ""

        return str(value).strip()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
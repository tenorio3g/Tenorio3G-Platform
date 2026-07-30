# ==========================================================
# T3G-ASSET-007
#
# Entity  : Manufacturer
# Domain  : Assets
# Version : 1.0.0
#
# ==========================================================

from dataclasses import dataclass


@dataclass(slots=True)
class Manufacturer:
    """
    Representa un fabricante de equipos industriales.
    """

    code: str
    name: str
    country: str = ""
    website: str = ""
    support_email: str = ""
    support_phone: str = ""
    is_active: bool = True

    def __post_init__(self) -> None:
        self.code = self._normalize_code(self.code)
        self.name = self._normalize_required(self.name)
        self.country = self.country.strip()
        self.website = self.website.strip()
        self.support_email = self.support_email.strip()
        self.support_phone = self.support_phone.strip()

    @property
    def display_name(self) -> str:
        return f"{self.code} - {self.name}"

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def update_contact(
        self,
        *,
        website: str = "",
        email: str = "",
        phone: str = "",
    ) -> None:
        """
        Actualiza la información de contacto.
        """

        if website:
            self.website = website.strip()

        if email:
            self.support_email = email.strip()

        if phone:
            self.support_phone = phone.strip()

    def matches(self, text: str) -> bool:

        value = text.strip().casefold()

        if not value:
            return False

        return any(
            value in item.casefold()
            for item in (
                self.code,
                self.name,
                self.country,
                self.website,
            )
        )

    @staticmethod
    def _normalize_code(value: str) -> str:

        value = value.strip().upper()

        if not value:
            raise ValueError("Manufacturer code cannot be empty.")

        return value

    @staticmethod
    def _normalize_required(value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("Manufacturer name cannot be empty.")

        return value
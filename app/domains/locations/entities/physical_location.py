from __future__ import annotations


class PhysicalLocation:
    """
    Representa una ubicacion fisica reutilizable
    dentro de la organizacion.
    """

    def __init__(
        self,
        code: str,
        name: str,
        area: str,
        is_active: bool = True,
    ) -> None:

        clean_code = code.strip()
        clean_name = name.strip()
        clean_area = area.strip()

        if not clean_code:
            raise ValueError(
                "El codigo de ubicacion es obligatorio."
            )

        if not clean_name:
            raise ValueError(
                "El nombre de ubicacion es obligatorio."
            )

        if not clean_area:
            raise ValueError(
                "El area de ubicacion es obligatoria."
            )

        self.code = clean_code
        self.name = clean_name
        self.area = clean_area
        self.is_active = is_active

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def __repr__(self) -> str:
        return (
            "PhysicalLocation("
            f"code='{self.code}', "
            f"name='{self.name}', "
            f"area='{self.area}', "
            f"is_active={self.is_active})"
        )

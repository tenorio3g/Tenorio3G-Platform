from __future__ import annotations


class SparePart:
    """
    Representa una refacción reutilizable en uno o varios activos.
    """

    def __init__(
        self,
        code: str,
        name: str,
        manufacturer: str = "",
        part_number: str = "",
        unit: str = "pieza",
        description: str = "",
    ) -> None:
        self.code = code.strip()
        self.name = name.strip()
        self.manufacturer = manufacturer.strip()
        self.part_number = part_number.strip()
        self.unit = unit.strip() or "pieza"
        self.description = description.strip()

        self._validate()

    def _validate(self) -> None:
        if not self.code:
            raise ValueError(
                "El código de la refacción es obligatorio."
            )

        if not self.name:
            raise ValueError(
                "El nombre de la refacción es obligatorio."
            )

    def __repr__(self) -> str:
        return (
            "SparePart("
            f"code='{self.code}', "
            f"name='{self.name}', "
            f"part_number='{self.part_number}'"
            ")"
        )
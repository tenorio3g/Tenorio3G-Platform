from __future__ import annotations


class AssetLocation:
    """
    Representa la ubicación física de un activo.
    """

    __slots__ = (
        "_code",
    )

    def __init__(
        self,
        code: str,
    ) -> None:

        clean_code = code.strip()

        if not clean_code:
            raise ValueError(
                "El código de ubicación es obligatorio."
            )

        self._code = clean_code

    @property
    def code(self) -> str:
        return self._code

    def __repr__(self) -> str:

        return (
            f"AssetLocation(code='{self.code}')"
        )
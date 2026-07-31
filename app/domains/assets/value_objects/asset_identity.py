from __future__ import annotations


class AssetIdentity:
    """
    Representa la identidad permanente de un activo.
    """

    __slots__ = (
        "_code",
        "_name",
        "_manufacturer",
        "_brand",
        "_model",
        "_serial_number",
    )

    def __init__(
        self,
        code: str,
        name: str,
        manufacturer: str,
        brand: str,
        model: str,
        serial_number: str,
    ) -> None:

        self._code = code
        self._name = name
        self._manufacturer = manufacturer
        self._brand = brand
        self._model = model
        self._serial_number = serial_number

        def __eq__(
            self,
            other: object,
        ) -> bool:

            if not isinstance(
                other,
                AssetIdentity,
            ):
                return False

            return (
                self.code == other.code
                and self.name == other.name
                and self.manufacturer == other.manufacturer
                and self.brand == other.brand
                and self.model == other.model
                and self.serial_number == other.serial_number
            )

        def __hash__(self) -> int:

            return hash(
                (
                    self.code,
                    self.name,
                    self.manufacturer,
                    self.brand,
                    self.model,
                    self.serial_number,
                )
            )

        def __repr__(self) -> str:

            return (
                "AssetIdentity("
                f"code='{self.code}', "
                f"name='{self.name}')"
            )

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def brand(self) -> str:
        return self._brand

    @property
    def model(self) -> str:
        return self._model

    @property
    def serial_number(self) -> str:
        return self._serial_number
from dataclasses import (
    dataclass,
)


@dataclass(slots=True)
class ExplorerItemViewModel:
    """
    Representa un componente registrado dentro
    del Foundation Explorer.
    """

    id: str

    name: str

    category: str

    status: str

    version: str | None

    since: str | None

    owner: str | None

    depends_on: tuple[str, ...]

    @property
    def has_dependencies(self) -> bool:
        """
        Indica si el componente posee dependencias.
        """

        return bool(self.depends_on)
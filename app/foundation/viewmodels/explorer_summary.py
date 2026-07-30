from dataclasses import (
    dataclass,
)


@dataclass(slots=True)
class ExplorerSummaryViewModel:
    """
    Resumen estadístico del Foundation Explorer.
    """

    total: int

    primitives: int

    components: int

    patterns: int

    utilities: int

    stable: int

    development: int

    deprecated: int

    pending: int
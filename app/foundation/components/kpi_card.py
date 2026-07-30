from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class KpiCardViewModel:
    """
    Contrato de presentación del componente KPI Card.

    Foundation únicamente renderiza la información.
    """

    title: str
    value: str

    subtitle: Optional[str] = None

    icon: Optional[str] = None

    variant: str = "primary"

    def __post_init__(self) -> None:

        if not self.title.strip():
            raise ValueError(
                "KpiCardViewModel.title no puede estar vacío."
            )

        if not self.value.strip():
            raise ValueError(
                "KpiCardViewModel.value no puede estar vacío."
            )
from dataclasses import dataclass

from app.domains.assets.technical_data.entities.technical_data import (
    TechnicalData,
)


@dataclass(frozen=True, slots=True)
class GetTechnicalDataResult:
    success: bool
    message: str
    technical_data: TechnicalData | None = None
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SaveTechnicalDataResult:
    success: bool
    message: str
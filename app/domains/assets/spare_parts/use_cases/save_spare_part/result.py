from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SaveSparePartResult:
    success: bool
    message: str
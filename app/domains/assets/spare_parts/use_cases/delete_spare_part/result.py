from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeleteSparePartResult:
    success: bool
    message: str
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RegisterPhysicalLocationCommand:
    code: str
    name: str
    area: str

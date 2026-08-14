from dataclasses import dataclass


@dataclass
class RoleItemViewModel:
    code: str
    name: str
    description: str
    status: str
    is_active: bool


@dataclass
class RolesViewModel:
    items: list[RoleItemViewModel]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)
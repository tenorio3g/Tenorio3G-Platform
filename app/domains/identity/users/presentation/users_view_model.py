from dataclasses import dataclass


@dataclass
class UserItemViewModel:
    username: str
    person_code: str
    person_name: str
    role_code: str
    role_name: str
    status: str
    is_active: bool


@dataclass
class UsersViewModel:
    items: list[UserItemViewModel]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)
from dataclasses import dataclass


@dataclass
class PersonItemViewModel:
    code: str
    name: str
    position: str
    status: str


@dataclass
class PeopleViewModel:
    items: list[PersonItemViewModel]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def total(self) -> int:
        return len(self.items)

@dataclass
class PersonItemViewModel:
    code: str
    name: str
    position: str
    status: str
    is_active: bool
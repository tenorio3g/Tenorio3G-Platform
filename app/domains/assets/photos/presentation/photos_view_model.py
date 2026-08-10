from dataclasses import dataclass


@dataclass
class PhotoItemViewModel:
    code: str
    title: str
    photo_type: str
    file_name: str
    description: str
    created_at: str


@dataclass
class PhotosViewModel:
    items: list[PhotoItemViewModel]

    @property
    def has_items(self) -> bool:
        return bool(self.items)

    @property
    def primary_photo(
        self,
    ) -> PhotoItemViewModel | None:

        for item in self.items:
            if item.photo_type == "general":
                return item

        return None
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Photo:
    code: str
    asset_code: str
    title: str
    photo_type: str
    file_name: str
    description: str = ""
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.code.strip():
            raise ValueError("Photo code is required.")

        if not self.asset_code.strip():
            raise ValueError("Asset code is required.")

        if not self.title.strip():
            raise ValueError("Photo title is required.")

        if not self.photo_type.strip():
            raise ValueError("Photo type is required.")

        if not self.file_name.strip():
            raise ValueError("File name is required.")

        if self.created_at is None:
            self.created_at = datetime.now()
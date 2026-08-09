from dataclasses import dataclass


@dataclass
class DocumentItemViewModel:
    code: str
    title: str
    document_type: str
    file_name: str
    description: str
    revision: str
    created_at: str


@dataclass
class DocumentsViewModel:
    items: list[DocumentItemViewModel]
from dataclasses import dataclass


@dataclass
class ProjectInventory:
    project_name: str
    python_files: int = 0
    html_files: int = 0
    css_files: int = 0
    javascript_files: int = 0
    markdown_files: int = 0
    empty_files: int = 0
    total_files: int = 0
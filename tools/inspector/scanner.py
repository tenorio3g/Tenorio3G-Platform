from pathlib import Path

from .models import ProjectInventory


IGNORED_DIRECTORIES = {
    ".git",
    ".github",
    ".idea",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "virtualenv",
    "__pycache__",
    "node_modules",
    "site-packages",
    "dist",
    "build",
    "_migration",
}


def is_ignored(path: Path) -> bool:
    return any(
        part.lower() in IGNORED_DIRECTORIES
        for part in path.parts
    )
def scan_project(project_root: Path) -> ProjectInventory:
    inventory = ProjectInventory(
        project_name=project_root.name
    )

    for file_path in project_root.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(project_root)

        if is_ignored(relative_path):
            continue

        inventory.total_files += 1

        suffix = file_path.suffix.lower()

        if suffix == ".py":
            inventory.python_files += 1
        elif suffix in {".html", ".htm"}:
            inventory.html_files += 1
        elif suffix == ".css":
            inventory.css_files += 1
        elif suffix == ".js":
            inventory.javascript_files += 1
        elif suffix == ".md":
            inventory.markdown_files += 1

        try:
            if file_path.stat().st_size == 0:
                inventory.empty_files += 1
        except OSError:
            continue

    return inventory
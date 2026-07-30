from pathlib import Path

from .reporter import print_report
from .scanner import scan_project


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> None:
    project_root = get_project_root()
    inventory = scan_project(project_root)
    print_report(inventory)


if __name__ == "__main__":
    main()
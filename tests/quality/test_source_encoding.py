from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SOURCE_ROOTS = (
    PROJECT_ROOT / "app",
    PROJECT_ROOT / "tests",
)

ROOT_TEXT_FILES = (
    PROJECT_ROOT / "requirements.txt",
)

TEXT_EXTENSIONS = {
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
    ".toml",
}

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
}

MOJIBAKE_MARKERS = (
    "\u00c3",
    "\u00c2",
    "\ufffd",
    "\u00e2\u20ac",
)


def iter_source_files():
    for root in SOURCE_ROOTS:
        if not root.exists():
            continue

        for path in root.rglob("*"):
            if not path.is_file():
                continue

            if any(
                part in IGNORED_DIRECTORIES
                for part in path.parts
            ):
                continue

            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue

            yield path

    for path in ROOT_TEXT_FILES:
        if path.exists():
            yield path


def relative_name(path):
    return path.relative_to(PROJECT_ROOT).as_posix()


def test_source_files_are_utf8_without_bom():
    failures = []

    for path in iter_source_files():
        data = path.read_bytes()

        if data.startswith(b"\xef\xbb\xbf"):
            failures.append(
                f"{relative_name(path)}: UTF-8 BOM detected"
            )
            continue

        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            failures.append(
                f"{relative_name(path)}: invalid UTF-8 "
                f"at byte {exc.start}"
            )

    assert not failures, (
        "Source encoding violations:\n"
        + "\n".join(failures)
    )


@pytest.mark.parametrize(
    "path",
    tuple(iter_source_files()),
    ids=relative_name,
)
def test_source_files_do_not_contain_common_mojibake(path):
    text = path.read_text(
        encoding="utf-8"
    )

    found = [
        marker
        for marker in MOJIBAKE_MARKERS
        if marker in text
    ]

    assert not found, (
        f"{relative_name(path)} contains "
        "possible mojibake markers: "
        + ", ".join(
            marker.encode("unicode_escape").decode("ascii")
            for marker in found
        )
    )

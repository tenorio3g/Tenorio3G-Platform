from pathlib import Path

from tools.generators.filesystem import Filesystem


def test_should_create_directory(
    tmp_path: Path,
) -> None:

    directory = tmp_path / "inventory" / "entities"

    result = Filesystem.create_directory(
        directory
    )

    assert result == directory
    assert directory.exists()
    assert directory.is_dir()


def test_should_create_empty_file(
    tmp_path: Path,
) -> None:

    file_path = tmp_path / "inventory" / "__init__.py"

    result = Filesystem.create_file(
        file_path
    )

    assert result == file_path
    assert file_path.exists()
    assert file_path.read_text(
        encoding="utf-8"
    ) == ""


def test_should_create_file_with_content(
    tmp_path: Path,
) -> None:

    file_path = tmp_path / "inventory" / "README.md"

    Filesystem.create_file(
        file_path,
        content="# Inventory\n",
    )

    assert file_path.read_text(
        encoding="utf-8"
    ) == "# Inventory\n"


def test_should_not_overwrite_existing_file(
    tmp_path: Path,
) -> None:

    file_path = tmp_path / "README.md"

    file_path.write_text(
        "Original content",
        encoding="utf-8",
    )

    Filesystem.create_file(
        file_path,
        content="New content",
    )

    assert file_path.read_text(
        encoding="utf-8"
    ) == "Original content"


def test_should_write_text(
    tmp_path: Path,
) -> None:

    file_path = tmp_path / "MODULE_STATUS.md"

    result = Filesystem.write_text(
        file_path,
        "# Module Status\n",
    )

    assert result == file_path
    assert file_path.read_text(
        encoding="utf-8"
    ) == "# Module Status\n"


def test_should_report_existing_path(
    tmp_path: Path,
) -> None:

    directory = tmp_path / "assets"
    directory.mkdir()

    assert Filesystem.exists(directory) is True
    assert Filesystem.exists(
        tmp_path / "missing"
    ) is False
"""Tests for the `darkgraylib.files` module."""

# pylint: disable=redefined-outer-name

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest

from darkgraylib import files


@contextmanager
def change_directory(path: Path) -> Iterator[None]:
    """Context manager to temporarily chdir to a different directory."""
    previous_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(previous_dir)


@pytest.fixture
def src_root(tmp_path: Path) -> Path:
    """Create a directory structure for testing `find_project_root`."""
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (tmp_path / "pyproject.toml").write_text("", encoding="utf-8")
    (src_dir / "pyproject.toml").write_text("", encoding="utf-8")
    (src_dir / "foo.py").touch()
    return tmp_path


def test_find_project_root_two_subdirectories_common_root(src_root: Path) -> None:
    """Test `find_project_root` with two subdirectories."""
    result = files.find_project_root((src_root / "src", src_root / "test"))
    assert result == src_root.resolve()


def test_find_project_root_one_subdirectory_has_pyproject(src_root: Path) -> None:
    """Test `find_project_root` with one subdirectory that has a `pyproject.toml`."""
    result = files.find_project_root((src_root / "src",))
    assert result == (src_root / "src").resolve()


def test_find_project_root_one_file_nested_pyproject(src_root: Path) -> None:
    """Test `find_project_root` with `pyproject.toml` in a parent directory."""
    result = files.find_project_root((src_root / "src" / "foo.py",))
    assert result == (src_root / "src").resolve()


def test_find_project_root(src_root: Path) -> None:
    """Test `find_project_root` with `pyproject.toml` in a grandparent directory."""
    src_sub = src_root / "src" / "sub"
    src_sub.mkdir()
    src_sub_python = src_sub / "bar.py"

    result = files.find_project_root((src_sub_python,))

    # we skip src_sub since it has no `pyproject.toml`
    assert result == (src_root / "src").resolve()

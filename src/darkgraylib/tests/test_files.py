"""Tests for the `darkgraylib.files` module."""

import os
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator
from unittest import TestCase

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


class BlackTestCase(TestCase):
    def test_find_project_root(self) -> None:
        with TemporaryDirectory() as workspace:
            root = Path(workspace)
            test_dir = root / "test"
            test_dir.mkdir()

            src_dir = root / "src"
            src_dir.mkdir()

            root_pyproject = root / "pyproject.toml"
            root_pyproject.write_text("[tool.black]", encoding="utf-8")
            src_pyproject = src_dir / "pyproject.toml"
            src_pyproject.write_text("[tool.black]", encoding="utf-8")
            src_python = src_dir / "foo.py"
            src_python.touch()

            self.assertEqual(
                files.find_project_root((src_dir, test_dir)),
                root.resolve(),
            )
            self.assertEqual(
                files.find_project_root((src_dir,)),
                src_dir.resolve(),
            )
            self.assertEqual(
                files.find_project_root((src_python,)),
                src_dir.resolve(),
            )

            src_sub = src_dir / "sub"
            src_sub.mkdir()

            # src_sub_pyproject = src_sub / "pyproject.toml"
            # src_sub_pyproject.touch()  # empty

            src_sub_python = src_sub / "bar.py"

            # we skip src_sub_pyproject since it is missing the [tool.black] section
            self.assertEqual(
                files.find_project_root((src_sub_python,)),
                src_dir.resolve(),
            )

"""Pytest fixture factory for making temporary copies of directory trees."""

from __future__ import annotations

import re
from contextlib import contextmanager
from shutil import copytree
from typing import TYPE_CHECKING, Callable, ContextManager

import pytest

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Generator


@pytest.fixture
def make_temp_copy(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory
) -> Callable[[Path], ContextManager[Path]]:
    """Pytest fixture to create a temporary clone of a directory structure."""

    @contextmanager
    def temp_copy_factory(path: Path) -> Generator[Path]:
        max_len = 30
        name = re.sub(r"\W", "_", f"clone_{request.node.name}")[:max_len]
        clone = tmp_path_factory.mktemp(name, numbered=True) / path.name
        copytree(path, clone)
        yield clone

    return temp_copy_factory

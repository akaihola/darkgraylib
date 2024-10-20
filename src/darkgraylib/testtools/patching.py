"""Helpers for patching in tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Iterator


@pytest.fixture(scope="module")
def monkeymodule() -> Iterator[pytest.MonkeyPatch]:
    """Return a module-scope monkeypatch fixture."""
    with pytest.MonkeyPatch.context() as monkey_patch:
        yield monkey_patch

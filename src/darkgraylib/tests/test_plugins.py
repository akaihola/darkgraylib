"""Unit tests for plugin system in darkgraylib.

This module contains tests for the plugin system that uses setuptools entry points
to discover and load plugins dynamically.

.. note::
   These tests use mocking to avoid having actual entry points registered.
"""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest import mock

import pytest

from darkgraylib.plugins import (
    create_plugin,
    get_entry_point_names,
    get_entry_points_for_group,
    get_plugin_class,
)

if TYPE_CHECKING:
    from collections.abc import Generator


# Test constants
TEST_GROUP = "test.plugins"


# Test plugin class (not a test)
class DummyPlugin:
    """Dummy plugin class used for testing."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize the dummy plugin.

        :param args: Positional arguments passed to the plugin.
        :param kwargs: Keyword arguments passed to the plugin.
        """
        self.args = args
        self.kwargs = kwargs


@pytest.fixture
def mock_entry_points() -> Generator[mock.MagicMock, None, None]:
    """Mock entry_points

    :return: Mock object that simulates the entry_points function.
    """
    with mock.patch("darkgraylib.plugins.entry_points") as mock_eps:
        # Create mock entry points
        ep1 = mock.Mock()
        ep1.name = "plugin1"
        ep1.load.return_value = DummyPlugin

        ep2 = mock.Mock()
        ep2.name = "plugin2"
        ep2.load.return_value = DummyPlugin

        def side_effect(
            group: str | None = None, name: str | None = None
        ) -> list[mock.Mock]:
            if group != TEST_GROUP:
                return []
            if name:
                if name == "plugin1":
                    return [ep1]
                if name == "plugin2":
                    return [ep2]
                return []
            return [ep1, ep2]

        mock_eps.side_effect = side_effect

        yield mock_eps


@pytest.mark.usefixtures("mock_entry_points")
def test_get_entry_points_for_group() -> None:
    """Test getting entry points for a specific group.

    :tests: `darkgraylib.plugins.get_entry_points_for_group`
    """
    # Define expected count as a constant
    expected_entry_point_count = 2

    # Test getting all entry points
    result = get_entry_points_for_group(TEST_GROUP)
    assert len(result) == expected_entry_point_count
    assert [ep.name for ep in result] == ["plugin1", "plugin2"]

    # Test getting entry points by name
    result = get_entry_points_for_group(TEST_GROUP, "plugin1")
    assert len(result) == 1
    assert result[0].name == "plugin1"


@pytest.mark.usefixtures("mock_entry_points")
def test_get_entry_point_names() -> None:
    """Test getting names of entry points for a group.

    :tests: `darkgraylib.plugins.get_entry_point_names`
    """
    result = get_entry_point_names(TEST_GROUP)
    assert result == ["plugin1", "plugin2"]


@pytest.mark.usefixtures("mock_entry_points")
def test_get_plugin_class() -> None:
    """Test getting a plugin class by name.

    :tests: `darkgraylib.plugins.get_plugin_class`
    """
    result = get_plugin_class(TEST_GROUP, "plugin1")
    assert result == DummyPlugin


@pytest.mark.usefixtures("mock_entry_points")
def test_create_plugin() -> None:
    """Test creating a plugin instance from entry point.

    :tests: `darkgraylib.plugins.create_plugin`
    """
    # Test creating plugin with args and kwargs
    test_arg = "test_arg"
    test_kwarg = "test_kwarg"
    plugin = create_plugin(TEST_GROUP, "plugin1", test_arg, kwarg=test_kwarg)

    # Check plugin is correct type with expected args
    assert isinstance(plugin, DummyPlugin)
    assert plugin.args == (test_arg,)
    assert plugin.kwargs == {"kwarg": test_kwarg}

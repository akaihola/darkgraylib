"""Helpers for handling plugins implemented as setuptools entry points."""

from __future__ import annotations

import sys
from importlib.metadata import EntryPoint, entry_points
from typing import Any, cast


def get_entry_points_for_group(
    entry_point_group: str, name: str | None = None
) -> tuple[EntryPoint, ...]:
    """Get the entry points of plugins for the given group."""
    if sys.version_info < (3, 10):
        return tuple(
            entry_point
            for entry_point in entry_points()[entry_point_group]
            if not name or entry_point.name == name
        )
    if name:
        result = entry_points(group=entry_point_group, name=name)
    else:
        result = entry_points(group=entry_point_group)
    return cast("tuple[EntryPoint, ...]", result)


def get_entry_point_names(entry_point_group: str) -> list[str]:
    """Get the names of all plugins for the given group."""
    return [ep.name for ep in get_entry_points_for_group(entry_point_group)]


def get_plugin_class(entry_point_group: str, name: str) -> type:
    """Retrieve the plugin class by name from the given group."""
    matching_entry_points = get_entry_points_for_group(entry_point_group, name)
    plugin_class = next(iter(matching_entry_points)).load()
    return cast("type", plugin_class)


def create_plugin(entry_point_group: str, name: str) -> type:
    """Create a plugin instance by entry point group and plugin name."""
    plugin_class = get_plugin_class(entry_point_group, name)()
    return cast("type", plugin_class)

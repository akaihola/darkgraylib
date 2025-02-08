"""Helpers for handling plugins implemented as setuptools entrypoints."""

from __future__ import annotations

import sys
from importlib.metadata import EntryPoint, entry_points
from typing import Type, TypeVar, cast

T = TypeVar("T")


def get_output_format_entry_points(
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
    return cast(tuple[EntryPoint, ...], result)


def get_entry_point_names(entry_point_group: str) -> list[str]:
    """Get the names of all built-in output format plugins."""
    return [ep.name for ep in get_output_format_entry_points(entry_point_group)]


def get_plugin_class(entry_point_group: str, name: str) -> Type:
    """Create an output format plugin instance by name."""
    matching_entry_points = get_output_format_entry_points(entry_point_group, name)
    plugin_class = next(iter(matching_entry_points)).load()
    return plugin_class


def create_plugin(entry_point_group: str, name: str, *args, **kwargs) -> Type:
    return get_plugin_class(entry_point_group, name)(*args, **kwargs)

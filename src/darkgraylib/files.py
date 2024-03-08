"""Helper functions for working with files and directories."""

from functools import lru_cache
from pathlib import Path
from typing import Sequence, Union


@lru_cache
def _cached_resolve(path: Path) -> Path:
    """Cache calls to `path.resolve()` to avoid redundant system calls."""
    return path.resolve()


@lru_cache
def find_project_root(srcs: Sequence[Union[str, Path]]) -> Path:
    """Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.

    Returns a two-tuple with the first element as the project root path and
    the second element as a string describing the method by which the
    project root was discovered.
    """
    if not srcs:
        srcs = [str(_cached_resolve(Path.cwd()))]

    path_srcs = [_cached_resolve(Path(Path.cwd(), src)) for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (directory / ".git").exists():
            return directory

        if (directory / ".hg").is_dir():
            return directory

        if (directory / "pyproject.toml").is_file():
            return directory

    return directory  # pylint: disable=undefined-loop-variable

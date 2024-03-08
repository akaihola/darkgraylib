"""Functions for maintaining compatibility with multiple Black versions"""

from pathlib import Path
from typing import Sequence

from darkgraylib.files import find_project_root as black_find_project_root


def find_project_root(srcs: Sequence[str]) -> Path:
    """Hide changed return value type in Black behind this wrapper

    :param srcs: Files and directories to find the common root for
    :return: Project root path

    """
    return black_find_project_root(tuple(srcs or ["."]))[0]

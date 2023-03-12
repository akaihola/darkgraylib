"""Common helpers used by `darker.__main__` and `graylint.__main__`"""

import logging
from pathlib import Path
from typing import List, Set, Tuple

from darkgraylib.utils import TextDocument, get_common_root

logger = logging.getLogger(__name__)

ProcessedDocument = Tuple[Path, TextDocument, TextDocument]


def resolve_paths(stdin_filename: str, src: List[str]) -> Tuple[Set[Path], Path]:
    if stdin_filename is not None:
        paths = {Path(stdin_filename)}
        # `parse_command_line` guarantees that `args.src` is empty
    else:
        paths = {Path(p) for p in src}
        # `parse_command_line` guarantees that `args.stdin_filename` is `None`
    return paths, get_common_root(paths)

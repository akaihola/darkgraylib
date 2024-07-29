"""Diff text and get line numbers of changes or chunks of original and changed content

The functions in this module implement

- diffing text files, returning opcodes
- turning opcodes into a list of line numbers of changed lines
- turning opcodes into chunks of original and modified text

In our case, we run a diff between original and user-edited source code.
Graylint creates a mapping of line numbers between the two versions of the source code.
Darker uses this module to do another diff between user-edited and Black-reformatted
source code as returned by `black.black_diff.run_black_for_content`.

    >>> src = TextDocument.from_lines(
    ...     [
    ...         'for i in range(5): print(i)',
    ...         'print("done")'
    ...     ]
    ... )

    >>> dst = TextDocument.from_lines(
    ...     [
    ...         'for i in range(5):',
    ...         '    print(i)',
    ...         'print("done")'
    ...     ]
    ... )

:func:`diff_and_get_opcodes`.
divides a diff between the original and reformatted content
into alternating chunks of
intact (represented by the 'equal' tag) and
modified ('delete', 'replace' or 'insert' tag) lines.
Each chunk is an opcode represented by the tag and the corresponding 0-based line ranges
in the original and reformatted content, e.g.::

    >>> opcodes = diff_and_get_opcodes(src, dst)
    >>> len(opcodes)
    2
    >>> opcodes[0]  # split 'for' loop into two lines
    ('replace', 0, 1, 0, 2)
    >>> opcodes[1]  # keep 'print("done")' as such
    ('equal', 1, 2, 2, 3)

"""

import logging
from difflib import SequenceMatcher
from typing import Dict, List, Literal, Tuple

from darkgraylib.utils import TextDocument

logger = logging.getLogger(__name__)


def diff_and_get_opcodes(
    src: TextDocument, dst: TextDocument
) -> List[Tuple[Literal["replace", "delete", "insert", "equal"], int, int, int, int]]:
    """Return opcodes and line numbers for chunks in the diff of two lists of strings

    The opcodes are 5-tuples for each chunk with

    - the tag of the operation ('equal', 'delete', 'replace' or 'insert')
    - the number of the first line in the chunk in the from-file
    - the number of the last line in the chunk in the from-file
    - the number of the first line in the chunk in the to-file
    - the number of the last line in the chunk in the to-file

    Line numbers are zero based.

    """
    matcher = SequenceMatcher(None, src.lines, dst.lines, autojunk=False)
    opcodes = matcher.get_opcodes()
    logger.debug(
        "Diff between edited and reformatted has %s opcode%s",
        len(opcodes),
        "s" if len(opcodes) > 1 else "",
    )
    return opcodes


def validate_opcodes(
    opcodes: List[
        Tuple[Literal["replace", "delete", "insert", "equal"], int, int, int, int]
    ]
) -> None:
    """Make sure every other opcode is an 'equal' tag"""
    if not all(
        (tag1 == "equal") != (tag2 == "equal")
        for (tag1, _, _, _, _), (tag2, _, _, _, _) in zip(opcodes[:-1], opcodes[1:])
    ):
        raise ValueError(f"Unexpected opcodes in {opcodes!r}")


def map_unmodified_lines(src: TextDocument, dst: TextDocument) -> Dict[int, int]:
    """Return a mapping of line numbers of unmodified lines between dst and src docs

    After doing a diff between ``src`` and ``dst``, some identical chunks of lines may
    be identified. For each such chunk, a mapping from every line number of the chunk in
    ``dst`` to corresponding line number in ``src`` is added.

    :param src: The original text document
    :param dst: The modified text document
    :return: A mapping from ``dst`` lines to corresponding unmodified ``src`` lines.
             Line numbers are 1-based.
    :raises RuntimeError: if blocks in opcodes don't make sense

    """
    opcodes = diff_and_get_opcodes(src, dst)
    validate_opcodes(opcodes)
    if not src.string and not dst.string:
        # empty files may get linter messages on line 1
        return {1: 1}
    result = {}
    for tag, src_start, src_end, dst_start, dst_end in opcodes:
        if tag != "equal":
            continue
        for line_delta in range(dst_end - dst_start):
            result[dst_start + line_delta + 1] = src_start + line_delta + 1
        if line_delta != src_end - src_start - 1:
            raise RuntimeError(
                "Something is wrong, 'equal' diff blocks should have the same length."
                f" src_start={src_start}, src_end={src_end},"
                f" dst_start={dst_start}, dst_end={dst_end}"
            )
    return result

"""Unit tests for `darkgraylib.diff`"""

import pytest

from darkgraylib.diff import diff_and_get_opcodes, map_unmodified_lines
from darkgraylib.testtools.diff_helpers import (
    EXPECT_OPCODES,
    FUNCTIONS2_PY,
    FUNCTIONS2_PY_REFORMATTED,
)
from darkgraylib.utils import TextDocument


def test_diff_and_get_opcodes():
    """``diff_and_get_opcodes()`` produces correct opcodes for the example sources"""
    src = TextDocument.from_str(FUNCTIONS2_PY)
    dst = TextDocument.from_str(FUNCTIONS2_PY_REFORMATTED)

    opcodes = diff_and_get_opcodes(src, dst)

    assert opcodes == EXPECT_OPCODES


@pytest.mark.kwparametrize(
    dict(
        expect={1: 1},
    ),
    dict(
        lines2=["file", "was", "empty", "but", "eventually", "not"],
        expect={},
    ),
    dict(
        lines1=["file", "had", "content", "but", "becomes", "empty"],
        expect={},
    ),
    dict(
        lines1=["1 unmoved", "2 modify", "3 to 4 moved"],
        lines2=["1 unmoved", "2 modified", "3 inserted", "3 to 4 moved"],
        expect={1: 1, 4: 3},
    ),
    dict(
        lines1=["can't", "follow", "both", "when", "order", "is", "changed"],
        lines2=["when", "order", "is", "changed", "can't", "follow", "both"],
        expect={1: 4, 2: 5, 3: 6, 4: 7},
    ),
    lines1=[],
    lines2=[],
)
def test_map_unmodified_lines(lines1, lines2, expect):
    """``map_unmodified_lines`` returns a 1-based mapping from new to old linenums"""
    doc1 = TextDocument.from_lines(lines1)
    doc2 = TextDocument.from_lines(lines2)

    result = map_unmodified_lines(doc1, doc2)

    assert result == expect

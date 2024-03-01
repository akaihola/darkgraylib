"""Unit tests for `darkgraylib.diff`"""

from textwrap import dedent

import pytest

from darkgraylib.diff import diff_and_get_opcodes, map_unmodified_lines
from darkgraylib.utils import TextDocument

FUNCTIONS2_PY = dedent(
    """\
    def f(
      a,
      **kwargs,
    ) -> A:
        with cache_dir():
            if something:
                result = (
                    CliRunner().invoke(black.main, [str(src1), str(src2), "--diff", "--check"])
                )
        limited.append(-limited.pop())  # negate top
        return A(
            very_long_argument_name1=very_long_value_for_the_argument,
            very_long_argument_name2=-very.long.value.for_the_argument,
            **kwargs,
        )
    def g():
        "Docstring."
        def inner():
            pass
        print("Inner defs should breathe a little.")
    def h():
        def inner():
            pass
        print("Inner defs should breathe a little.")
"""  # noqa: E501
)


FUNCTIONS2_PY_REFORMATTED = dedent(
    """\
    def f(
        a,
        **kwargs,
    ) -> A:
        with cache_dir():
            if something:
                result = CliRunner().invoke(
                    black.main, [str(src1), str(src2), "--diff", "--check"]
                )
        limited.append(-limited.pop())  # negate top
        return A(
            very_long_argument_name1=very_long_value_for_the_argument,
            very_long_argument_name2=-very.long.value.for_the_argument,
            **kwargs,
        )


    def g():
        "Docstring."

        def inner():
            pass

        print("Inner defs should breathe a little.")


    def h():
        def inner():
            pass

        print("Inner defs should breathe a little.")
    """
)


EXPECT_OPCODES = [
    ("equal", 0, 1, 0, 1),
    ("replace", 1, 3, 1, 3),
    ("equal", 3, 6, 3, 6),
    ("replace", 6, 8, 6, 8),
    ("equal", 8, 15, 8, 15),
    ("insert", 15, 15, 15, 17),
    ("equal", 15, 17, 17, 19),
    ("insert", 17, 17, 19, 20),
    ("equal", 17, 19, 20, 22),
    ("insert", 19, 19, 22, 23),
    ("equal", 19, 20, 23, 24),
    ("insert", 20, 20, 24, 26),
    ("equal", 20, 23, 26, 29),
    ("insert", 23, 23, 29, 30),
    ("equal", 23, 24, 30, 31),
]


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

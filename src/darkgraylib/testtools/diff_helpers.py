"""Test data for ``diff_helpers.py`` tests."""

from textwrap import dedent

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

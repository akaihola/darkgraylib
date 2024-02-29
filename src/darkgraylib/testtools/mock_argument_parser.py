"""Mock argument parser factory for testing."""
from argparse import ArgumentParser

from darkgraylib.command_line import make_argument_parser


def make_test_argument_parser(require_src: bool = False) -> ArgumentParser:
    """Create a mock argument parser object for testing.

    :param require_src: ``True`` to require at least one path as a positional argument
                        on the command line. ``False`` to not require on.
    :return: The mock argument parser object

    """
    return make_argument_parser(
        require_src,
        "Darkgraylib",
        "dummy description",
        "config help",
    )

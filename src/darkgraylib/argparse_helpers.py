"""Custom formatter and action for argparse."""

import logging
import re
import sys
from abc import ABC
from argparse import SUPPRESS, Action, ArgumentParser, HelpFormatter, Namespace
from difflib import ndiff
from pathlib import Path
from textwrap import fill
from typing import Any, List, Optional, Sequence, Union

WORD_RE = re.compile(r"\w")


def _fill_line(line: str, width: int, indent: str) -> str:
    first_word_match = WORD_RE.search(line)
    first_word_offset = first_word_match.start() if first_word_match else 0
    return fill(
        line,
        width,
        initial_indent=indent,
        subsequent_indent=indent + first_word_offset * " ",
    )


class NewlinePreservingFormatter(HelpFormatter):
    """A command line help formatter which preserves newline characters"""
    def _fill_text(self, text: str, width: int, indent: str) -> str:
        if "\n" in text:
            return "\n".join(
                _fill_line(line, width, indent) for line in text.split("\n")
            )
        return super()._fill_text(text, width, indent)


class SuppressedFlagAction(Action, ABC):
    """Base class for argparse option flags which are suppressed from ``--help``."""

    # pylint: disable=too-few-public-methods, redefined-builtin

    def __init__(
        self,
        option_strings: List[str],
        dest: str = SUPPRESS,
        help: Optional[str] = None,
    ) -> None:
        """Initialize the action to accept zero arguments."""
        super().__init__(option_strings, dest, 0, help=help)


class OptionsForReadmeAction(SuppressedFlagAction):
    """Implementation of the ``--options-for-readme`` argument.

    This argparse action prints optional command line arguments in a format suitable for
    inclusion in ``README.rst``.

    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,  # noqa: ARG002
        values: Optional[Union[str, Sequence[Any]]],  # noqa: ARG002
        option_string: Optional[str] = None,  # noqa: ARG002
    ) -> None:
        """Print ``--help`` usage documentation in a format suitable for README.rst.

        :param parser: The parser for which to generate usage
        :param namespace: Ignored
        :param values: Ignored
        :param option_string: Ignored

        """
        usage = generate_options_for_readme(parser)
        sys.stderr.write(usage)
        parser.exit()


class VerifyReadmeAction(SuppressedFlagAction):
    """Implementation of the ``--verify-readme`` argument.

    This argparse action generates optional command line arguments in a format suitable
    for inclusion in ``README.rst``, compares them to what is already in the file, and
    prints a diff if they differ.

    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,  # noqa: ARG002
        values: Optional[Union[str, Sequence[Any]]],  # noqa: ARG002
        option_string: Optional[str] = None,  # noqa: ARG002
    ) -> None:
        """Compare the generated ``--help`` usage to the current ``README.rst``.

        Exit with code 0 if they are the same, 1 if they differ, and 2 if ``--help``
        output could not be found in the README.rst file.

        :param parser: The parser for which to generate usage
        :param namespace: Ignored
        :param values: Ignored
        :param option_string: Ignored

        """
        for section in get_readme_sections():
            lines = (section + "\n").splitlines(keepends=True)
            if is_help_section(lines):
                usage = generate_options_for_readme(parser).splitlines(keepends=True)
                if lines == usage:
                    parser.exit(0, "README.rst is up to date\n")
                parser.exit(1, "".join(ndiff(lines, usage)) + "\n")
        parser.exit(2, "Could not find --help output in README.rst\n")


class UpdateReadmeAction(SuppressedFlagAction):
    """Implementation of the ``--update-readme`` argument.

    This argparse action generates optional command line arguments in a format suitable
    for inclusion in ``README.rst`` and updates the file.

    """

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Optional[Union[str, Sequence[Any]]],
        option_string: str = None,
    ) -> None:
        new_content = []
        found = False
        for section in get_readme_sections():
            lines = section.splitlines(keepends=True)
            if is_help_section(lines):
                new_content.append(generate_options_for_readme(parser).rstrip())
                found = True
            else:
                new_content.append(section)
        if not found:
            parser.exit(2, "Could not find --help output in README.rst\n")
        Path("README.rst").write_text("".join(new_content), encoding="utf-8")
        parser.exit(0, "README.rst updated\n")


def is_help_section(section: List[str]) -> bool:
    """Return ``True`` if given README section is the ``--help`` output from argparse.

    :param section: The section to check
    :return: True if the text looks like the ``--help`` output from argparse

    """
    cmds = sum(1 for line in section if re.match(r"-\w\W|--\w\w+", line))
    descriptions = sum(1 for line in section if line.startswith("       "))
    return cmds > 0 and descriptions > 0 and cmds + descriptions == len(section)


def get_readme_sections() -> List[str]:
    """Return blank line separated sections of the ``README.rst`` file.

    :return: A list of strings, each string being a section of the ``README.rst`` file

    """
    return re.split(r"(\n\n+)", Path("README.rst").read_text(encoding="utf-8"))


def generate_options_for_readme(parser: ArgumentParser) -> str:
    """Generate ``--help`` usage documentation in a format suitable for ``README.rst``.

    :param parser: The parser for which to generate usage
    :return: A string containing the usage documentation

    """
    # pylint: disable=protected-access
    optional_arguments_group = next(
        group
        for group in parser._action_groups  # noqa: SLF001
        # The group title for options differs between Python versions
        if group.title in {"optional arguments", "options"}
    )
    actions = []
    for action in optional_arguments_group._group_actions:  # noqa: SLF001
        if action.dest in {"help", "version", "options_for_readme"}:
            continue
        if action.help is not None:
            action.help = action.help.replace("`", "``").replace("|", r"\|")
        actions.append(action)
    formatter = HelpFormatter(parser.prog, max_help_position=7, width=88)
    formatter.add_arguments(actions)
    return formatter.format_help()


class LogLevelAction(Action):  # pylint: disable=too-few-public-methods
    """Support for command line actions which increment/decrement the log level"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        option_strings: List[str],
        dest: str,
        const: int,
        default: int = logging.WARNING,
        required: bool = False,
        help: str = None,  # pylint: disable=redefined-builtin
        metavar: str = None,
    ):
        super().__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=0,
            const=const,
            default=default,
            required=required,
            help=help,
            metavar=metavar,
        )

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: str = None,
    ) -> None:
        current_level = getattr(namespace, self.dest, self.default)
        new_level = current_level + self.const
        new_level = max(new_level, logging.DEBUG)
        new_level = min(new_level, logging.CRITICAL)
        setattr(namespace, self.dest, new_level)

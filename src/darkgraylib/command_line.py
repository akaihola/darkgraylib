"""Command line parsing for the ``darker`` and ``graylint`` binaries."""

from __future__ import annotations

import sys
from argparse import SUPPRESS, ArgumentParser, Namespace
from functools import partial
from typing import Any, Callable, Protocol, TypeVar

from darkgraylib import help as hlp
from darkgraylib.argparse_helpers import (
    LogLevelAction,
    NewlinePreservingFormatter,
    OptionsForReadmeAction,
    UpdateReadmeAction,
    VerifyReadmeAction,
)
from darkgraylib.config import (
    BaseConfig,
    get_effective_config,
    get_modified_config,
    load_config,
    override_color_with_environment,
    validate_stdin_src,
)
from darkgraylib.version import __version__


def make_argument_parser(
    require_src: bool,
    application: str,
    description: str,
    config_help: str,
    version: str = __version__,
) -> ArgumentParser:
    """Create the argument parser object

    :param require_src: ``True`` to require at least one path as a positional argument
                        on the command line. ``False`` to not require on.
    :param application: The name of the application: ``"Darker"``, ``"Graylint"``, etc.
    :param description: The descriptive text for the application to be shown in
                        ``--help`` output.
    :param config_help: The help text for the ``--config`` option.

    """
    parser = ArgumentParser(
        description=description, formatter_class=NewlinePreservingFormatter
    )
    parser.register("action", "log_level", LogLevelAction)

    add_arg = partial(add_parser_argument, parser)

    add_arg(hlp.SRC, "src", nargs="+" if require_src else "*", metavar="PATH")
    add_arg(
        hlp.REVISION.format(application=application),
        "-r",
        "--revision",
        default="HEAD",
        metavar="REV",
    )
    add_arg(
        hlp.STDIN_FILENAME.format(application=application),
        "--stdin-filename",
        metavar="PATH",
    )
    add_arg(config_help, "-c", "--config", metavar="PATH")
    add_arg(
        hlp.VERBOSE,
        "-v",
        "--verbose",
        action="log_level",
        dest="log_level",
        const=-10,
    )
    add_arg(hlp.QUIET, "-q", "--quiet", action="log_level", dest="log_level", const=10)
    add_arg(hlp.COLOR, "--color", action="store_const", dest="color", const=True)
    add_arg(hlp.NO_COLOR, "--no-color", action="store_const", dest="color", const=False)
    add_arg(
        hlp.VERSION.format(application=application),
        "--version",
        action="version",
        version=version,
    )
    add_arg(hlp.WORKERS, "-W", "--workers", type=int, dest="workers", default=1)
    # A hidden option for printing command lines option in a format suitable for
    # `README.rst`:
    add_arg(SUPPRESS, "--options-for-readme", action=OptionsForReadmeAction)
    add_arg(SUPPRESS, "--verify-readme", action=VerifyReadmeAction)
    add_arg(SUPPRESS, "--update-readme", action=UpdateReadmeAction)
    return parser


def add_parser_argument(
    parser: ArgumentParser,
    help_text: str | None,
    *name_or_flags: str,
    **kwargs: Any,  # noqa: ANN401
) -> None:
    """Add an argument to the parser

    :parser: The parser to add the argument to
    :help_text: The help text for the argument
    :name_or_flags: The name of the positional argument or the alternative flags for the
                    option
    :kwargs: Additional keyword arguments to pass to ``parser.add_argument()``

    """
    kwargs["help"] = help_text
    parser.add_argument(*name_or_flags, **kwargs)


T = TypeVar("T", bound=BaseConfig)


class ArgumentParserFactory(Protocol):  # pylint: disable=too-few-public-methods
    """A function that creates an argument parser object"""

    def __call__(self, require_src: bool) -> ArgumentParser:
        ...


def parse_command_line(
    argument_parser_factory: ArgumentParserFactory,
    argv: list[str] | None,
    section_name: str,
    config_type: type[T],
    load_config_hook: Callable[[T], None] | None = None,
) -> tuple[Namespace, T, T]:
    """Return the parsed command line, using defaults from a configuration file

    Also return the effective configuration which combines defaults, the configuration
    read from ``pyproject.toml`` (or the path given in ``--config``), environment
    variables, and command line arguments.

    Finally, also return the set of configuration options which differ from defaults.

    :param argument_parser_factory: A function that creates an argument parser object.
    :param argv: Command line arguments to parse (excluding the path of the script). If
                 ``None``, use ``sys.argv``.
    :param section_name: The name of the section in the configuration file to read
    :param config_type: The type of the configuration object to be returned. For Darker,
                        this should be ``DarkerConfig``, for Graylint
                        ``GraylintConfig``.
    :param load_config_hook: A hook to call after loading the configuration file. This
                             is used to warn about configuration options which are
                             deprecated in the configuration file.
    :return: A tuple of the parsed command line, the effective configuration, and the
             set of modified configuration options from the defaults.

    """
    if argv is None:
        argv = sys.argv[1:]

    # 1. Parse the paths of files/directories to process into `args.src`, and the config
    #    file path into `args.config`.
    parser_for_srcs = argument_parser_factory(require_src=False)
    args = parser_for_srcs.parse_args(argv)

    # 2. Locate `pyproject.toml` based on the `-c`/`--config` command line option, or
    #    if it's not provided, based on the paths to process, or in the current
    #    directory if no paths were given. Load Darker or Graylint configuration from
    #    it.
    pyproject_config = load_config(args.config, args.src, section_name, config_type)
    if load_config_hook:
        load_config_hook(pyproject_config)

    # 3. The PY_COLORS, NO_COLOR and FORCE_COLOR environment variables override the
    #    `--color` command line option.
    config = override_color_with_environment(pyproject_config)

    # 4. Re-run the parser with configuration defaults. This way we get combined values
    #    based on the configuration file and the command line options for all options
    #    except `src` (the list of files to process).
    parser_for_srcs.set_defaults(**config)
    args = parser_for_srcs.parse_args(argv)

    # 5. Make sure an error for missing file/directory paths is thrown if we're not
    #    running in stdin mode and no file/directory is configured in `pyproject.toml`.
    if args.stdin_filename is None and not config.get("src"):
        parser = argument_parser_factory(require_src=True)
        parser.set_defaults(**config)
        args = parser.parse_args(argv)

    # Make sure there aren't invalid option combinations after merging configuration and
    # command line options.
    validate_stdin_src(args.stdin_filename, args.src)

    # 7. Also create a parser which uses the original default configuration values.
    #    This is used to find out differences between the effective configuration and
    #    default configuration values, and print them out in verbose mode.
    parser_with_original_defaults = argument_parser_factory(
        require_src=args.stdin_filename is None
    )
    return (
        args,
        get_effective_config(args, config_type),
        get_modified_config(parser_with_original_defaults, args, config_type),
    )

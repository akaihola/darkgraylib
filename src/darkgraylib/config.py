"""Load and save configuration in TOML format"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING, Dict, Iterable, TypedDict, TypeVar, Union, cast

import toml

from darkgraylib.files import find_project_root

if TYPE_CHECKING:
    from argparse import ArgumentParser, Namespace


class TomlArrayLinesEncoder(toml.TomlEncoder):  # type: ignore
    """Format TOML so list items are each on their own line"""

    def dump_list(self, v: Iterable[object]) -> str:
        """Format a list value"""
        return "[{}\n]".format("".join(f"\n    {self.dump_value(item)}," for item in v))


UnvalidatedConfig = Dict[str, Union["list[str]", str, bool, int]]


class BaseConfig(TypedDict, total=False):
    """Dictionary representing configuration from ``pyproject.toml``

    These are the configuration options common to both Darker and Graylint.

    """

    src: list[str]
    revision: str
    stdout: bool
    config: str
    log_level: int | str
    color: bool
    workers: int


class ConfigurationError(Exception):
    """Exception class for invalid configuration values"""


def convert_config_characters(
    config: UnvalidatedConfig, pattern: str, replacement: str
) -> UnvalidatedConfig:
    """Convert a character in config keys to a different character"""
    return {key.replace(pattern, replacement): value for key, value in config.items()}


def convert_hyphens_to_underscores(config: UnvalidatedConfig) -> UnvalidatedConfig:
    """Convert hyphenated config keys to underscored keys"""
    return convert_config_characters(config, "-", "_")


def convert_underscores_to_hyphens(config: BaseConfig) -> UnvalidatedConfig:
    """Convert underscores in config keys to hyphens"""
    return convert_config_characters(cast(UnvalidatedConfig, config), "_", "-")


T = TypeVar("T", bound=BaseConfig)


def validate_config_keys(
    config: UnvalidatedConfig,
    section_name: str,
    config_type: type[T],  # pylint: disable=unused-argument
) -> None:
    """Raise an exception if any keys in the configuration are invalid.

    :param config: The configuration read from ``pyproject.toml``
    :param section_name: The name of the section in the configuration file. For Darker,
                         this is ``"darker"`` and for Graylint, this is ``"graylint"``.
    :param config_type: The class representing the configuration options. For Darker,
                        this is ``darker.config.DarkerConfig`` and for Graylint, this
                        is ``graylint.config.GraylintConfig``.
    :raises ConfigurationError: Raised if unknown options are present

    """
    if set(config).issubset(config_type.__annotations__):
        return
    unknown_keys = ", ".join(
        sorted(set(config).difference(config_type.__annotations__))
    )
    raise ConfigurationError(
        f"Invalid [tool.{section_name}] keys in pyproject.toml: {unknown_keys}"
    )


def replace_log_level_name(config: BaseConfig) -> None:
    """Replace numeric log level in configuration with the name of the log level"""
    if "log_level" in config:
        config["log_level"] = logging.getLevelName(config["log_level"])


def validate_stdin_src(stdin_filename: str | None, src: list[str]) -> None:
    """Make sure both ``stdin`` mode and paths/directories are specified"""
    if stdin_filename is None:
        return
    if len(src) == 0 or src == ["-"]:
        return
    raise ConfigurationError(
        "No Python source files are allowed when using the `stdin-filename` option"
    )


def override_color_with_environment(pyproject_config: BaseConfig) -> BaseConfig:
    """Override ``color`` if the ``PY_COLORS`` environment variable is '0' or '1'

    :param config: The configuration read from ``pyproject.toml``
    :return: The modified configuration

    """
    config = pyproject_config.copy()
    py_colors = os.getenv("PY_COLORS")
    if py_colors in {"0", "1"}:
        config["color"] = py_colors == "1"
    elif os.getenv("NO_COLOR") is not None:
        config["color"] = False
    elif os.getenv("FORCE_COLOR") is not None:
        config["color"] = True
    return config


def load_config(
    path: str | None,
    srcs: Iterable[str],
    section_name: str,
    config_type: type[T],
) -> T:
    """Find and load configuration from a TOML configuration file

    The location for the configuration file is determined by trying the following:
    - the file path in the `path` argument, given using the ``-c``/``--config`` command
      line option
    - ``pyproject.toml`` inside the directory specified by the `path` argument
    - ``pyproject.toml`` from a common parent directory to all items in `srcs`
    - ``pyproject.toml`` in the current working directory if `srcs` is empty

    :param path: The file or directory specified using the ``-c``/``--config`` command
                 line option, or `None` if the option was omitted.
    :param srcs: File(s) and directory/directories to be processed by Darker or
                 Graylint.
    :param section_name: The name of the section in the configuration file. For Darker,
                         this is ``"darker"`` and for Graylint, this is ``"graylint"``.
    :param config_type: The class representing the configuration options. For Darker,
                        this is ``darker.config.DarkerConfig`` and for Graylint, this
                        is ``graylint.config.GraylintConfig``.

    """
    if path:
        for candidate_path in [Path(path), Path(path, "pyproject.toml")]:
            if candidate_path.is_file():
                config_path = candidate_path
                break
        else:
            if Path(path).is_dir() or path.endswith(os.sep):
                raise ConfigurationError(
                    f"Configuration file {Path(path, 'pyproject.toml')} not found"
                )
            raise ConfigurationError(f"Configuration file {path} not found")
    else:
        config_path = find_project_root(tuple(srcs or ["."])) / "pyproject.toml"
        if not config_path.is_file():
            return cast(T, {})
    pyproject_toml = toml.load(config_path)
    pyproject_tool_config = convert_hyphens_to_underscores(
        pyproject_toml.get("tool", {}).get(section_name, {}) or {}
    )
    validate_config_keys(pyproject_tool_config, section_name, config_type)
    config = cast(T, pyproject_tool_config)
    replace_log_level_name(config)
    return config


def get_effective_config(
    args: Namespace,
    config_type: type[T],  # pylint: disable=unused-argument  # noqa: ARG001
) -> T:
    """Return all configuration options

    :param args: The command line arguments
    :param config_type: The type of the configuration options
    :return: The effective configuration options

    """
    config = cast(T, vars(args).copy())
    replace_log_level_name(config)
    return config


def get_modified_config(
    parser: ArgumentParser,
    args: Namespace,
    config_type: type[T],  # pylint: disable=unused-argument  # noqa: ARG001
) -> T:
    """Return configuration options which are set to non-default values

    :param parser: The argument parser
    :param args: The command line arguments
    :param config_type: The type of the configuration options
    :return: Those configuration options differing from default values

    """
    not_default = cast(
        T,
        {
            argument: value
            for argument, value in vars(args).items()
            if value != parser.get_default(argument)
        },
    )
    replace_log_level_name(not_default)
    return not_default


def dump_config(config: BaseConfig, section_name: str) -> str:
    """Return the configuration in TOML format

    :param config: The configuration options
    :param section_name: The name of the section in the configuration file

    """
    dump = toml.dumps(
        convert_underscores_to_hyphens(config), encoder=TomlArrayLinesEncoder()
    )
    return f"[tool.{section_name}]\n{dump}"


def show_config_if_debug(
    config: BaseConfig,
    config_nondefault: BaseConfig,
    log_level: int,
    section_name: str,
) -> None:
    """Show the configuration if the log level is DEBUG or lower

    :param config: The configuration options
    :param config_nondefault: Options which are set to non-default values
    :param log_level: The log level
    :param section_name: The name of the section in the configuration file.

    """
    if log_level <= logging.DEBUG:
        print("\n# Effective configuration:\n")
        print(dump_config(config, section_name))
        print("\n# Configuration options which differ from defaults:\n")
        print(dump_config(config_nondefault, section_name))
        print("\n")

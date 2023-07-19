"""Tests for the ``--stdin-filename`` option"""

# pylint: disable=too-many-arguments,use-dict-literal

from pathlib import Path
from typing import List, Optional

import pytest
import toml

from darkgraylib import command_line
from darkgraylib.config import BaseConfig, ConfigurationError
from darkgraylib.git import RevisionRange
from darkgraylib.testtools.git_repo_plugin import GitRepoFixture
from darkgraylib.testtools.helpers import raises_if_exception
from test_command_line import _make_test_argument_parser  # type: ignore

pytestmark = pytest.mark.usefixtures("find_project_root_cache_clear")


@pytest.mark.kwparametrize(
    dict(expect=SystemExit(2)),
    dict(
        config_src=["a.py"],
    ),
    dict(config_src=["b.py"], src=["a.py"]),
    dict(
        config_src=["b.py"],
        stdin_filename=["a.py"],
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(config_src=["a.py"], revision="..:STDIN:"),
    dict(config_src=["a.py"], revision="..:WORKTREE:"),
    dict(
        config_src=["b.py"],
        src=["a.py"],
        stdin_filename="a.py",
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(
        config_src=["b.py"],
        src=["a.py"],
        revision="..:STDIN:",
    ),
    dict(
        config_src=["b.py"],
        src=["a.py"],
        revision="..:WORKTREE:",
    ),
    dict(
        config_src=["b.py"],
        src=["a.py"],
        stdin_filename="a.py",
        revision="..:STDIN:",
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(
        config_src=["b.py"],
        src=["a.py"],
        stdin_filename="a.py",
        revision="..:WORKTREE:",
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(src=["a.py"]),
    dict(
        src=["a.py"],
        stdin_filename="a.py",
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(
        src=["a.py"],
        revision="..:STDIN:",
    ),
    dict(
        src=["a.py"],
        revision="..:WORKTREE:",
    ),
    dict(
        src=["a.py"],
        stdin_filename="a.py",
        revision="..:STDIN:",
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(
        src=["a.py"],
        stdin_filename="a.py",
        revision="..:WORKTREE:",
        expect=ConfigurationError(
            "No Python source files are allowed when using the `stdin-filename` option"
        ),
    ),
    dict(stdin_filename="a.py"),
    dict(stdin_filename="a.py", revision="..:STDIN:"),
    dict(
        stdin_filename="a.py",
        revision="..:WORKTREE:",
        expect=ValueError(
            "With --stdin-filename, rev2 in ..:WORKTREE: must be ':STDIN:', not"
            " ':WORKTREE:'"
        ),
    ),
    dict(revision="..:STDIN:", expect=SystemExit(2)),
    dict(revision="..:WORKTREE:", expect=SystemExit(2)),
    config_src=None,
    src=[],
    stdin_filename=None,
    revision=None,
    expect=0,
)
def test_main_stdin_filename(
    git_repo: GitRepoFixture,
    config_src: Optional[List[str]],
    src: List[str],
    stdin_filename: Optional[str],
    revision: Optional[str],
    expect: int,
) -> None:
    """Tests for the ``--stdin-filename`` option

    Exercises first `command_line.parse_command_line` and then
    `RevisionRange.parse_with_common_ancestor`. There is some error handling in both of
    those.

    """
    if config_src is not None:
        configuration = {"tool": {"darkgraylib": {"src": config_src}}}
        git_repo.add({"pyproject.toml": toml.dumps(configuration)})
    arguments = src[:]
    if stdin_filename is not None:
        arguments.insert(0, f"--stdin-filename={stdin_filename}")
    if revision is not None:
        arguments.insert(0, f"--revision={revision}")
    with raises_if_exception(expect):
        # end of test setup

        args, _, _ = command_line.parse_command_line(
            _make_test_argument_parser, arguments, "darkgraylib", BaseConfig
        )
        _ = RevisionRange.parse_with_common_ancestor(
            args.revision, Path(), args.stdin_filename is not None
        )

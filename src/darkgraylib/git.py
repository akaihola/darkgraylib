"""Helpers for listing modified files and getting unmodified content from Git"""

import logging
import os
import re
import shlex
import sys
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from subprocess import PIPE, CalledProcessError, check_output  # nosec
from typing import Dict, Iterator, List, Match, Optional, Tuple, Union, cast, overload

from darkgraylib.utils import GIT_DATEFORMAT, TextDocument


logger = logging.getLogger(__name__)


# Split a revision range into the "from" and "to" revisions and the dots in between.
# Handles these cases:
# <rev>..   <rev>..<rev>   ..<rev>
# <rev>...  <rev>...<rev>  ...<rev>
COMMIT_RANGE_RE = re.compile(r"(.*?)(\.{2,3})(.*)$")


# A colon is an invalid character in tag/branch names. Use that in the special value for
# - denoting the working tree as one of the "revisions" in revision ranges
# - referring to the `PRE_COMMIT_FROM_REF` and `PRE_COMMIT_TO_REF` environment variables
#   for determining the revision range
WORKTREE = ":WORKTREE:"
STDIN = ":STDIN:"
PRE_COMMIT_FROM_TO_REFS = ":PRE-COMMIT:"


def git_get_version() -> Tuple[int, ...]:
    """Return the Git version as a tuple of integers

    Ignores any suffixes to the dot-separated parts of the version string.

    :return: The version number of Git installed on the system
    :raise: ``RuntimeError`` if unable to parse the Git version

    """
    output_lines = git_check_output_lines(["--version"], Path("."))
    version_string = output_lines[0].rsplit(None, 1)[-1]
    # The version string might be e.g.
    # - "2.39.0.windows.1"
    # - "2.36.2"
    part_matches = [re.match(r"\d+", part) for part in version_string.split(".")][:3]
    if all(part_matches):
        return tuple(
            int(match.group(0)) for match in cast(List[Match[str]], part_matches)
        )
    raise RuntimeError(f"Unable to parse Git version: {output_lines!r}")


def git_rev_parse(revision: str, cwd: Path) -> str:
    """Return the commit hash for the given revision

    :param revision: The revision to get the commit hash for
    :param cwd: The root of the Git repository
    :return: The commit hash for ``revision`` as parsed from Git output

    """
    return git_check_output_lines(["rev-parse", revision], cwd)[0]


def git_get_mtime_at_commit(path: Path, revision: str, cwd: Path) -> str:
    """Return the committer date of the given file at the given revision

    :param path: The relative path of the file in the Git repository
    :param revision: The Git revision for which to get the file modification time
    :param cwd: The root of the Git repository

    """
    cmd = ["log", "-1", "--format=%ct", revision, "--", path.as_posix()]
    lines = git_check_output_lines(cmd, cwd)
    return datetime.fromtimestamp(int(lines[0]), timezone.utc).strftime(GIT_DATEFORMAT)


def git_get_content_at_revision(path: Path, revision: str, cwd: Path) -> TextDocument:
    """Get unmodified text lines of a file at a Git revision

    :param path: The relative path of the file in the Git repository
    :param revision: The Git revision for which to get the file content, or ``WORKTREE``
                     to get what's on disk right now.
    :param cwd: The root of the Git repository

    """
    if path.is_absolute():
        raise ValueError(
            f"the 'path' parameter must receive a relative path, got {path!r} instead"
        )

    if revision == WORKTREE:
        abspath = cwd / path
        return TextDocument.from_file(abspath)
    cmd = ["show", f"{revision}:./{path.as_posix()}"]
    try:
        return TextDocument.from_bytes(
            _git_check_output(cmd, cwd, exit_on_error=False),
            mtime=git_get_mtime_at_commit(path, revision, cwd),
        )
    except CalledProcessError as exc_info:
        if exc_info.returncode != 128:
            for error_line in exc_info.stderr.splitlines():
                logger.error(error_line)
            raise
        # The file didn't exist at the given revision. Act as if it was an empty
        # file, so all current lines appear as edited.
        return TextDocument()


@dataclass(frozen=True)
class RevisionRange:
    """Represent a range of commits in a Git repository for comparing differences

    ``rev1`` is the "old" revision, and ``rev2``, the "new" revision which should be
    compared against ``rev1``.

    When parsing a revision range expression with triple dots (e.g. ``master...HEAD``),
    the branch point, or common ancestor of the revisions, is used instead of the
    provided ``rev1``. This is useful e.g. when CI is doing a check
    on a feature branch, and there have been commits in the main branch after the branch
    point. Without the ability to compare to the branch point, Darker would suggest
    corrections to formatting on lines changes in the main branch even if those lines
    haven't been touched in the feature branch. Similarly, Graylint would include
    linting errors introduced by changes compared to the tip of the main branch, not the
    branch point.

    """

    rev1: str
    rev2: str

    @classmethod
    def parse_with_common_ancestor(
        cls, revision_range: str, cwd: Path, stdin_mode: bool
    ) -> "RevisionRange":
        """Convert a range expression to a ``RevisionRange`` object.

        If the expression contains triple dots (e.g. ``master...HEAD``), finds the
        common ancestor of the two revisions and uses that as the first revision.

        :param revision_range: The revision range as a string to parse
        :param cwd: The working directory to use when invoking Git. This has to be
                    either the root of the working tree, or another directory inside it.
        :param stdin_mode: If `True`, the default for ``rev2`` is ``:STDIN:``
        :return: The range parsed into a `RevisionRange` object

        """
        rev1, rev2, use_common_ancestor = cls._parse(revision_range, stdin_mode)
        if use_common_ancestor:
            return cls._with_common_ancestor(rev1, rev2, cwd)
        return cls(rev1, rev2)

    @staticmethod
    def _parse(revision_range: str, stdin_mode: bool) -> Tuple[str, str, bool]:
        """Convert a range expression to revisions, using common ancestor if appropriate

        A `ValueError` is raised if ``--stdin-filename`` is used by the revision range
        is ``:PRE-COMMIT:`` or the end of the range is not ``:STDIN:``.

        :param revision_range: The revision range as a string to parse
        :param stdin_mode: If `True`, the default for ``rev2`` is ``:STDIN:``
        :raises ValueError: for an invalid revision when ``--stdin-filename`` is used
        :return: The range parsed into a `RevisionRange` object

        >>> RevisionRange._parse("a..b", stdin_mode=False)
        ('a', 'b', False)
        >>> RevisionRange._parse("a...b", stdin_mode=False)
        ('a', 'b', True)
        >>> RevisionRange._parse("a..", stdin_mode=False)
        ('a', ':WORKTREE:', False)
        >>> RevisionRange._parse("a...", stdin_mode=False)
        ('a', ':WORKTREE:', True)
        >>> RevisionRange._parse("a..", stdin_mode=True)
        ('a', ':STDIN:', False)
        >>> RevisionRange._parse("a...", stdin_mode=True)
        ('a', ':STDIN:', True)

        """
        if revision_range == PRE_COMMIT_FROM_TO_REFS:
            if stdin_mode:
                raise ValueError(
                    f"With --stdin-filename, revision {revision_range!r} is not allowed"
                )
            try:
                return (
                    os.environ["PRE_COMMIT_FROM_REF"],
                    os.environ["PRE_COMMIT_TO_REF"],
                    True,
                )
            except KeyError:
                # Fallback to running against HEAD
                revision_range = "HEAD"
        match = COMMIT_RANGE_RE.match(revision_range)
        default_rev2 = STDIN if stdin_mode else WORKTREE
        if match:
            rev1, range_dots, rev2 = match.groups()
            use_common_ancestor = range_dots == "..."
            effective_rev2 = rev2 or default_rev2
            if stdin_mode and effective_rev2 != STDIN:
                raise ValueError(
                    f"With --stdin-filename, rev2 in {revision_range} must be"
                    f" {STDIN!r}, not {effective_rev2!r}"
                )
            return (rev1 or "HEAD", rev2 or default_rev2, use_common_ancestor)
        return (
            revision_range or "HEAD",
            default_rev2,
            revision_range not in ["", "HEAD"],
        )

    @classmethod
    def _with_common_ancestor(cls, rev1: str, rev2: str, cwd: Path) -> "RevisionRange":
        """Find common ancestor for revisions and return a ``RevisionRange`` object.

        :param rev1: The first revision in the range
        :param rev2: The second revision in the range
        :param cwd: The working directory to use when invoking Git. This has to be
                    either the root of the working tree, or another directory inside it.
        :return: The range parsed into a `RevisionRange` object

        """
        rev2_for_merge_base = "HEAD" if rev2 in [WORKTREE, STDIN] else rev2
        merge_base_cmd = ["merge-base", rev1, rev2_for_merge_base]
        common_ancestor = git_check_output_lines(merge_base_cmd, cwd)[0]
        rev1_hash = git_check_output_lines(["show", "-s", "--pretty=%H", rev1], cwd)[0]
        return cls(rev1 if common_ancestor == rev1_hash else common_ancestor, rev2)


@lru_cache(maxsize=1)
def make_git_env() -> Dict[str, str]:
    """Create custom minimal environment variables to use when invoking Git

    This makes sure that
    - Git always runs in English
    - ``$PATH`` is preserved (essential on NixOS)
    - the environment is otherwise cleared

    """
    return {"LC_ALL": "C", "PATH": os.environ["PATH"]}


def git_check_output_lines(
    cmd: List[str], cwd: Path, exit_on_error: bool = True
) -> List[str]:
    """Log command line, run Git, split stdout to lines, exit with 123 on error"""
    return _git_check_output(
        cmd,
        cwd,
        exit_on_error=exit_on_error,
        encoding="utf-8",
    ).splitlines()


@overload
def _git_check_output(
    cmd: List[str], cwd: Path, *, exit_on_error: bool = ..., encoding: None = ...
) -> bytes:
    ...


@overload
def _git_check_output(
    cmd: List[str], cwd: Path, *, exit_on_error: bool = ..., encoding: str
) -> str:
    ...


def _git_check_output(
    cmd: List[str],
    cwd: Path,
    *,
    exit_on_error: bool = True,
    encoding: Optional[str] = None,
) -> Union[str, bytes]:
    """Log command line, run Git, return stdout, exit with 123 on error"""
    logger.debug("[%s]$ git %s", cwd, shlex.join(cmd))
    try:
        return check_output(  # nosec
            ["git"] + cmd,
            cwd=str(cwd),
            encoding=encoding,
            stderr=PIPE,
            env=make_git_env(),
        )
    except CalledProcessError as exc_info:
        if not exit_on_error:
            raise
        if exc_info.returncode != 128:
            if encoding:
                sys.stderr.write(exc_info.stderr)
            else:
                sys.stderr.buffer.write(exc_info.stderr)
            raise

        # Bad revision or another Git failure. Follow Black's example and return the
        # error status 123.
        for error_line in exc_info.stderr.splitlines():
            logger.error(error_line)
        sys.exit(123)


@contextmanager
def git_clone_local(
    source_repository: Path, revision: str, destination: Path
) -> Iterator[Path]:
    """Clone a local repository and check out the given revision

    :param source_repository: Path to the root of the local repository checkout
    :param revision: The revision to check out, or ``HEAD``
    :param destination: Directory to create for the clone
    :return: A context manager which yields the path to the clone

    """
    opts = [
        # By default, `add` refuses to create a new worktree when `<commit-ish>` is
        # a branch name and is already checked out by another worktree, or if
        # `<path>` is already assigned to some worktree but is missing (for
        # instance, if `<path>` was deleted manually). This option overrides these
        # safeguards. To add a missing but locked worktree path, specify `--force`
        # twice.
        # `remove` refuses to remove an unclean worktree unless `--force` is used.
        # To remove a locked worktree, specify `--force` twice.
        # https://git-scm.com/docs/git-worktree#_options
        "--force",
        "--force",
        str(destination),
    ]
    _ = _git_check_output(
        ["worktree", "add", "--quiet", *opts, revision], cwd=source_repository
    )
    yield destination
    _ = _git_check_output(["worktree", "remove", *opts], cwd=source_repository)


def git_get_root(path: Path) -> Optional[Path]:
    """Get the root directory of a local Git repository clone based on a path inside it

    :param path: A file or directory path inside the Git repository clone
    :return: The root of the clone, or ``None`` if none could be found
    :raises CalledProcessError: if Git exits with an unexpected error

    """
    try:
        return Path(
            _git_check_output(
                ["rev-parse", "--show-toplevel"],
                cwd=path if path.is_dir() else path.parent,
                encoding="utf-8",
                exit_on_error=False,
            ).rstrip()
        )
    except CalledProcessError as exc_info:
        if exc_info.returncode == 128 and exc_info.stderr.splitlines()[0].startswith(
            "fatal: not a git repository (or any "
        ):
            # The error string differs a bit in different Git versions, but up to the
            # point above it's identical in recent versions.
            return None
        sys.stderr.write(exc_info.stderr)
        raise

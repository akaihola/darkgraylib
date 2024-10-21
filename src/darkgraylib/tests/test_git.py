"""Tests for the `darkgraylib.git` module."""

# pylint: disable=no-member  # context managers misfire Pylint's member-checking
# pylint: disable=redefined-outer-name  # fixtures misfire Pylint's redefinition checks
# pylint: disable=use-dict-literal  # dict() ok with kwparametrize

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from subprocess import PIPE, CalledProcessError  # nosec
from typing import List, Union
from unittest.mock import ANY, Mock, call, patch

import pytest

from darkgraylib import git
from darkgraylib.testtools.git_repo_plugin import GitRepoFixture, branched_repo
from darkgraylib.testtools.helpers import raises_or_matches
from darkgraylib.utils import GIT_DATEFORMAT, TextDocument


def test_tmp_path_sanity(tmp_path):
    """Make sure Pytest temporary directories aren't inside a Git repository"""
    try:
        result = git.git_check_output_lines(
            ["rev-parse", "--absolute-git-dir"], tmp_path, exit_on_error=False
        )
    except CalledProcessError as exc_info:
        if exc_info.returncode != 128 or not exc_info.stderr.startswith(
            "fatal: not a git repository"
        ):
            raise
    else:
        output = "\n".join(result)
        raise AssertionError(
            f"Temporary directory {tmp_path} for tests is not clean."
            f" There is a Git directory in {output}"
        )


@pytest.mark.parametrize(
    "revision_range, expect",
    [
        ("", None),
        ("..", ("", "..", "")),
        ("...", ("", "...", "")),
        ("a..", ("a", "..", "")),
        ("a...", ("a", "...", "")),
        ("a..b", ("a", "..", "b")),
        ("a...b", ("a", "...", "b")),
        ("..b", ("", "..", "b")),
        ("...b", ("", "...", "b")),
    ],
)
def test_commit_range_re(revision_range, expect):
    """Test for ``COMMIT_RANGE_RE``"""
    match = git.COMMIT_RANGE_RE.match(revision_range)
    if expect is None:
        assert match is None
    else:
        assert match is not None
        assert match.groups() == expect


def test_worktree_symbol():
    """Test for the ``WORKTREE`` symbol"""
    assert git.WORKTREE == ":WORKTREE:"


def test_git_get_mtime_at_commit():
    """darkgraylib.git.git_get_mtime_at_commit()"""
    with patch.object(git, "git_check_output_lines"):
        git.git_check_output_lines.return_value = ["1609104839"]  # type: ignore

        result = git.git_get_mtime_at_commit(
            Path("dummy path"), "dummy revision", Path("dummy cwd")
        )
        assert result == "2020-12-27 21:33:59.000000 +0000"


@pytest.fixture(scope="module")
def git_get_content_at_revision_repo(request, tmp_path_factory):
    """Return Git repository fixture with a file that changes over time."""
    with GitRepoFixture.context(request, tmp_path_factory) as repo:
        repo.add({"my.txt": "original content"}, commit="Initial commit")
        paths = repo.add({"my.txt": "modified content"}, commit="Second commit")
        paths["my.txt"].write_bytes(b"new content")
        os.utime(paths["my.txt"], (1000000000, 1000000000))
        yield repo


@pytest.mark.kwparametrize(
    dict(
        revision=":WORKTREE:",
        expect_lines=("new content",),
        expect_mtime=lambda: datetime(2001, 9, 9, 1, 46, 40),
    ),
    dict(
        revision="HEAD",
        expect_lines=("modified content",),
        expect_mtime=datetime.utcnow,
    ),
    dict(
        revision="HEAD^",
        expect_lines=("original content",),
        expect_mtime=datetime.utcnow,
    ),
    dict(revision="HEAD~2", expect_lines=(), expect_mtime=False),
)
def test_git_get_content_at_revision(
    git_get_content_at_revision_repo, revision, expect_lines, expect_mtime
):
    """Test for `git.git_get_content_at_revision`."""
    result = git.git_get_content_at_revision(
        Path("my.txt"), revision, cwd=Path(git_get_content_at_revision_repo.root)
    )

    assert result.lines == expect_lines
    if expect_mtime:
        mtime_then = datetime.strptime(result.mtime, GIT_DATEFORMAT)
        difference = expect_mtime() - mtime_then
        assert timedelta(0) <= difference < timedelta(seconds=6)
    else:
        assert result.mtime == ""
    assert result.encoding == "utf-8"


def git_call(cmd, encoding=None):
    """Returns a mocked call to git"""
    return call(
        cmd.split(),
        cwd=str(Path("/path")),
        encoding=encoding,
        stderr=PIPE,
        env=ANY,
    )


@pytest.mark.kwparametrize(
    dict(
        revision=":WORKTREE:",
        expect_textdocument_calls=[call.from_file(Path("/path/my.txt"))],
    ),
    dict(
        revision="HEAD",
        expect_git_calls=[
            git_call("git show HEAD:./my.txt"),
            git_call("git log -1 --format=%ct HEAD -- my.txt", encoding="utf-8"),
        ],
        expect_textdocument_calls=[
            call.from_bytes(b"1627107028", mtime="2021-07-24 06:10:28.000000 +0000")
        ],
    ),
    dict(
        revision="HEAD^",
        expect_git_calls=[
            git_call("git show HEAD^:./my.txt"),
            git_call("git log -1 --format=%ct HEAD^ -- my.txt", encoding="utf-8"),
        ],
        expect_textdocument_calls=[
            call.from_bytes(b"1627107028", mtime="2021-07-24 06:10:28.000000 +0000")
        ],
    ),
    dict(
        revision="master",
        expect_git_calls=[
            git_call("git show master:./my.txt"),
            git_call("git log -1 --format=%ct master -- my.txt", encoding="utf-8"),
        ],
        expect_textdocument_calls=[
            call.from_bytes(b"1627107028", mtime="2021-07-24 06:10:28.000000 +0000")
        ],
    ),
    expect_git_calls=[],
)
def test_git_get_content_at_revision_obtain_file_content(
    revision, expect_git_calls, expect_textdocument_calls
):
    """``git_get_content_at_revision`` calls Git or reads files based on revision"""
    with patch("darkgraylib.git.check_output") as check_output, patch(
        "darkgraylib.git.TextDocument"
    ) as text_document_class:
        # this dummy value acts both as a dummy Unix timestamp for the file as well as
        # the contents of the file:
        check_output.return_value = b"1627107028"

        git.git_get_content_at_revision(Path("my.txt"), revision, Path("/path"))

        assert check_output.call_args_list == expect_git_calls
        assert text_document_class.method_calls == expect_textdocument_calls


git_check_output_lines_repo = pytest.fixture(scope="module")(branched_repo)


@pytest.mark.kwparametrize(
    dict(cmd=[], exit_on_error=True, expect_template=CalledProcessError(1, "")),
    dict(
        cmd=["status", "-sb"],
        exit_on_error=True,
        expect_template=[
            "## branch",
            "A  add_index.py",
            "D  del_index.py",
            " D del_worktree.py",
            "A  mod_index.py",
            "?? add_worktree.py",
            "?? mod_worktree.py",
        ],
    ),
    dict(
        cmd=["diff"],
        exit_on_error=True,
        expect_template=[
            "diff --git a/del_worktree.py b/del_worktree.py",
            "deleted file mode 100644",
            "index 94f3610..0000000",
            "--- a/del_worktree.py",
            "+++ /dev/null",
            "@@ -1 +0,0 @@",
            "-original",
            "\\ No newline at end of file",
        ],
    ),
    dict(
        cmd=["merge-base", "master"],
        exit_on_error=True,
        expect_template=CalledProcessError(129, ""),
    ),
    dict(
        cmd=["merge-base", "master", "HEAD"],
        exit_on_error=True,
        expect_template=["<hash of branch point>"],
    ),
    dict(
        cmd=["show", "missing.file"],
        exit_on_error=True,
        expect_template=SystemExit(123),
    ),
    dict(
        cmd=["show", "missing.file"],
        exit_on_error=False,
        expect_template=CalledProcessError(128, ""),
    ),
)
def test_git_check_output_lines(
    git_check_output_lines_repo, cmd, exit_on_error, expect_template
):
    """Unit test for :func:`git_check_output_lines`"""
    branched_repo = git_check_output_lines_repo
    if isinstance(expect_template, BaseException):
        expect: Union[List[str], BaseException] = expect_template
    else:
        replacements = {"<hash of branch point>": branched_repo.get_hash("master^")}
        expect = [replacements.get(line, line) for line in expect_template]
    with raises_or_matches(expect, ["returncode", "code"]) as check:
        check(git.git_check_output_lines(cmd, branched_repo.root, exit_on_error))


@pytest.mark.kwparametrize(
    dict(
        cmd=["show", "{initial}:/.file2"],
        exit_on_error=True,
        expect_exc=SystemExit,
        expect_log=(
            r"(?:^|\n)ERROR    darkgraylib\.git:git\.py:\d+ fatal: "
            r"[pP]ath '/\.file2' does not exist in '{initial}'\n"
        ),
    ),
    dict(
        cmd=["show", "{initial}:/.file2"],
        exit_on_error=False,
        expect_exc=CalledProcessError,
    ),
    dict(
        cmd=["non-existing", "command"],
        exit_on_error=True,
        expect_exc=CalledProcessError,
        expect_stderr="git: 'non-existing' is not a git command. See 'git --help'.\n",
    ),
    dict(
        cmd=["non-existing", "command"],
        exit_on_error=False,
        expect_exc=CalledProcessError,
    ),
    expect_stderr="",
    expect_log=r"$",
)
def test_git_check_output_lines_stderr_and_log(
    git_repo, capfd, caplog, cmd, exit_on_error, expect_exc, expect_stderr, expect_log
):
    """Git non-existing file error is logged and suppressed from stderr"""
    git_repo.add({"file1": "file1"}, commit="Initial commit")
    initial = git_repo.get_hash()[:7]
    git_repo.add({"file2": "file2"}, commit="Second commit")
    capfd.readouterr()  # flush captured stdout and stderr
    cmdline = [s.format(initial=initial) for s in cmd]
    with pytest.raises(expect_exc):
        git.git_check_output_lines(cmdline, git_repo.root, exit_on_error)

    outerr = capfd.readouterr()
    assert outerr.out == ""
    assert outerr.err == expect_stderr
    expect_log_re = expect_log.format(initial=initial)
    assert re.search(expect_log_re, caplog.text), repr(caplog.text)


def test_git_get_content_at_revision_stderr(git_repo, capfd, caplog):
    """No stderr or log output from ``git_get_content_at_revision`` for missing file"""
    git_repo.add({"file1": "file1"}, commit="Initial commit")
    initial = git_repo.get_hash()[:7]
    git_repo.add({"file2": "file2"}, commit="Second commit")
    capfd.readouterr()  # flush captured stdout and stderr

    result = git.git_get_content_at_revision(Path("file2"), initial, git_repo.root)

    assert result == TextDocument()
    outerr = capfd.readouterr()
    assert outerr.out == ""
    assert outerr.err == ""
    assert [record for record in caplog.records if record.levelname != "DEBUG"] == []


@pytest.fixture(scope="module")
def encodings_repo(tmp_path_factory):
    """Create an example Git repository using various encodings for the same file"""
    tmpdir = tmp_path_factory.mktemp("branched_repo")
    git_repo = GitRepoFixture.create_repository(tmpdir)
    # Commit without an encoding cookie, defaults to utf-8
    git_repo.add({"file.py": "darkgraylib = 'plus foncé'\n"}, commit="Default encoding")
    git_repo.create_tag("default")
    # Commit without an encoding cookie but with a utf-8 signature
    content = "darkgraylib = 'plus foncé'\n".encode("utf-8-sig")
    git_repo.add({"file.py": content}, commit="utf-8-sig")
    git_repo.create_tag("utf-8-sig")
    # Commit with an iso-8859-1 encoding cookie
    content = "# coding: iso-8859-1\ndarkgraylib = 'plus foncé'\n".encode("iso-8859-1")
    git_repo.add({"file.py": content}, commit="iso-8859-1")
    git_repo.create_tag("iso-8859-1")
    # Commit with a utf-8 encoding cookie
    content = "# coding: utf-8\npython = 'パイソン'\n".encode()
    git_repo.add({"file.py": content}, commit="utf-8")
    git_repo.create_tag("utf-8")
    # Current worktree content (not committed) with a shitfjs encoding cookie
    content = "# coding: shiftjis\npython = 'パイソン'\n".encode("shiftjis")
    git_repo.add({"file.py": content})
    return git_repo


@pytest.mark.kwparametrize(
    dict(commit="default", encoding="utf-8", lines=("darkgraylib = 'plus foncé'",)),
    dict(
        commit="utf-8-sig", encoding="utf-8-sig", lines=("darkgraylib = 'plus foncé'",)
    ),
    dict(
        commit="iso-8859-1",
        encoding="iso-8859-1",
        lines=("# coding: iso-8859-1", "darkgraylib = 'plus foncé'"),
    ),
    dict(
        commit="utf-8", encoding="utf-8", lines=("# coding: utf-8", "python = 'パイソン'")
    ),
    dict(
        commit=":WORKTREE:",
        encoding="shiftjis",
        lines=("# coding: shiftjis", "python = 'パイソン'"),
    ),
)
def test_git_get_content_at_revision_encoding(encodings_repo, commit, encoding, lines):
    """Git file is loaded using its historical encoding"""
    result = git.git_get_content_at_revision(
        Path("file.py"), commit, encodings_repo.root
    )
    assert result.encoding == encoding
    assert result.lines == lines


@pytest.fixture(scope="module")
def git_clone_local_branch_repo(request, tmp_path_factory):
    """Git repository with three branches and a file with different content in each."""
    with GitRepoFixture.context(request, tmp_path_factory) as repo:
        repo.add({"a.py": "first"}, commit="first")
        repo.create_branch("first", "HEAD")
        repo.create_branch("second", "HEAD")
        repo.add({"a.py": "second"}, commit="second")
        repo.create_branch("third", "HEAD")
        repo.add({"a.py": "third"}, commit="third")
        yield repo


@pytest.mark.kwparametrize(
    dict(branch="first", expect="first"),
    dict(branch="second", expect="second"),
    dict(branch="third", expect="third"),
    dict(branch="HEAD", expect="third"),
)
def test_git_clone_local_branch(git_clone_local_branch_repo, tmp_path, branch, expect):
    """`git_clone_local` checks out the specified branch."""
    repo = git_clone_local_branch_repo
    with git.git_clone_local(repo.root, branch, tmp_path / "clone") as clone:
        assert (clone / "a.py").read_text() == expect


@pytest.mark.kwparametrize(
    dict(branch="HEAD"),
    dict(branch="mybranch"),
)
def test_git_clone_local_command(git_repo, tmp_path, branch):
    """``git_clone_local()`` issues the correct Git command and options"""
    git_repo.add({"a.py": "first"}, commit="first")
    git_repo.create_branch("mybranch", "HEAD")
    check_output = Mock(wraps=git.check_output)  # type: ignore[attr-defined]
    clone = tmp_path / "clone"
    check_output_opts = dict(
        cwd=str(git_repo.root), encoding=None, stderr=PIPE, env=ANY
    )
    pre_call = call(
        ["git", "worktree", "add", "--quiet", "--force", "--force", str(clone), branch],
        **check_output_opts,
    )
    post_call = call(
        ["git", "worktree", "remove", "--force", "--force", str(clone)],
        **check_output_opts,
    )
    with patch.object(git, "check_output", check_output):
        with git.git_clone_local(git_repo.root, branch, clone) as result:
            assert result == clone

            check_output.assert_has_calls([pre_call])
            check_output.reset_mock()
    check_output.assert_has_calls([post_call])


@pytest.mark.parametrize(
    "path",
    [
        ".",
        "root.py",
        "subdir",
        "subdir/sub.py",
        "subdir/subsubdir",
        "subdir/subsubdir/subsub.py",
    ],
)
def test_git_get_root(git_repo, path):
    """``git_get_root()`` returns repository root for any file or directory inside"""
    git_repo.add(
        {
            "root.py": "root",
            "subdir/sub.py": "sub",
            "subdir/subsubdir/subsub.py": "subsub",
        },
        commit="Initial commit",
    )

    root = git.git_get_root(git_repo.root / path)

    assert root == git_repo.root


@pytest.mark.parametrize(
    "path",
    [
        ".",
        "root.py",
        "subdir",
        "subdir/sub.py",
        "subdir/subsubdir",
        "subdir/subsubdir/subsub.py",
    ],
)
def test_git_get_root_not_found(tmp_path, path):
    """``git_get_root()`` returns ``None`` for any file or directory outside of Git"""
    (tmp_path / "subdir" / "subsubdir").mkdir(parents=True)
    (tmp_path / "root.py").touch()
    (tmp_path / "subdir" / "sub.py").touch()
    (tmp_path / "subdir" / "subsubdir" / "subsub.py").touch()

    root = git.git_get_root(tmp_path / path)

    assert root is None


def test_git_output_in_english(git_repo, monkeypatch):
    """Git output is in English despite German language environment."""
    # Set up German language environment
    german_env = {
        "LC_ALL": "de_DE.UTF-8",
        "LC_CTYPE": "de_DE.UTF-8",
        "LC_MESSAGES": "de_DE.UTF-8",
        "LANG": "de_DE.UTF-8",
    }
    for key, value in german_env.items():
        monkeypatch.setenv(key, value)

    # Run a Git command and check its output
    output = git.git_check_output_lines(["status"], git_repo.root)

    # Verify that the output is in English
    assert "No commits yet" in output
    assert "Noch keine Commits" not in output

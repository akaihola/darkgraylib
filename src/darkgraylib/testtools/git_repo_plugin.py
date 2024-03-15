"""Git repository fixture as a Pytest plugin"""

import os
import re
from pathlib import Path
from subprocess import check_call  # nosec
from typing import Dict, Iterable, List, Union

import pytest

from darkgraylib.git import git_check_output_lines, git_get_version


class GitRepoFixture:
    """Fixture for managing temporary Git repositories"""

    def __init__(self, root: Path, env: Dict[str, str]):
        self.root = root
        self.env = env

    @classmethod
    def create_repository(cls, root: Path) -> "GitRepoFixture":
        """Fixture method for creating a Git repository in the given directory"""
        # For testing, ignore ~/.gitconfig settings like templateDir and defaultBranch.
        # Also, this makes sure GIT_DIR or other GIT_* variables are not set, and that
        # Git's messages are in English.
        env = {"HOME": str(root), "LC_ALL": "C", "PATH": os.environ["PATH"]}
        instance = cls(root, env)
        # pylint: disable=protected-access
        force_master = (
            ["--initial-branch=master"] if git_get_version() >= (2, 28) else []
        )
        instance._run("init", *force_master)
        instance._run("config", "user.email", "ci@example.com")
        instance._run("config", "user.name", "CI system")
        return instance

    def _run(self, *args: str) -> None:
        """Helper method to run a Git command line in the repository root"""
        check_call(["git"] + list(args), cwd=self.root, env=self.env)  # nosec

    def _run_and_get_first_line(self, *args: str) -> str:
        """Helper method to run Git in repo root and return first line of output"""
        return git_check_output_lines(list(args), Path(self.root))[0]

    def add(
        self, paths_and_contents: Dict[str, Union[str, bytes, None]], commit: str = None
    ) -> Dict[str, Path]:
        """Add/remove/modify files and optionally commit the changes

        :param paths_and_contents: Paths of the files relative to repository root, and
                                   new contents for the files as strings. ``None`` can
                                   be specified as the contents in order to remove a
                                   file.
        :param commit: The message for the commit, or ``None`` to skip making a commit.

        """
        absolute_paths = {
            relative_path: self.root / relative_path
            for relative_path in paths_and_contents
        }
        for relative_path, content in paths_and_contents.items():
            path = absolute_paths[relative_path]
            if content is None:
                self._run("rm", "--", relative_path)
                continue
            if isinstance(content, str):
                content = content.encode("utf-8")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            self._run("add", "--", relative_path)
        if commit:
            self._run("commit", "-m", commit)
        return absolute_paths

    def rename(self, old_name: str, new_name: str, commit: str = None) -> None:
        """Rename/move files and optionally commit the changes

        :param old_name: The file to rename/move
        :param new_name: New name/location for the file
        :param commit: The message for the commit, or ``None`` to skip making a commit.
        """
        self._run("mv", old_name, new_name)
        if commit:
            self._run("commit", "-m", commit)

    def get_hash(self, revision: str = "HEAD") -> str:
        """Return the commit hash at the given revision in the Git repository"""
        return self._run_and_get_first_line("rev-parse", revision)

    def get_branch(self) -> str:
        """Return the active branch name in the Git repository"""
        return self._run_and_get_first_line("symbolic-ref", "--short", "HEAD")

    def create_tag(self, tag_name: str) -> None:
        """Create a tag at current HEAD"""
        self._run("tag", tag_name)

    def create_branch(self, new_branch: str, start_point: str) -> None:
        """Fixture method to create and check out new branch at given starting point"""
        self._run("checkout", "-b", new_branch, start_point)

    def expand_root(self, lines: Iterable[str]) -> List[str]:
        """Replace "{root/<path>}" in strings with the path in the temporary Git repo

        This is used to generate expected strings corresponding to locations of files in
        the temporary Git repository.

        :param lines: The lines of text to process
        :return: Given lines with paths processed

        """
        return [
            re.sub(
                r"\{root(/.*?)?\}",
                lambda m: str(self.root / (str(m.group(1)[1:]) if m.group(1) else "")),
                line,
            )
            for line in lines
        ]


@pytest.fixture
def git_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> GitRepoFixture:
    """Create a temporary Git repository and change current working directory into it"""
    repository = GitRepoFixture.create_repository(tmp_path)
    monkeypatch.chdir(tmp_path)
    # While `GitRepoFixture.create_repository()` already deletes `GIT_*` environment
    # variables for any Git commands run by the fixture, let's explicitly remove
    # `GIT_DIR` in case a test should call Git directly:
    monkeypatch.delenv("GIT_DIR", raising=False)

    return repository


@pytest.fixture(scope="module")
def branched_repo(tmp_path_factory: pytest.TempPathFactory) -> GitRepoFixture:
    """Create an example Git repository with a master branch and a feature branch

    The history created is::

        . worktree
        . index
        * branch
        | * master
        |/
        * Initial commit

    """
    tmpdir = tmp_path_factory.mktemp("branched_repo")
    repo = GitRepoFixture.create_repository(tmpdir)
    repo.add(
        {
            "del_master.py": "original",
            "del_branch.py": "original",
            "del_index.py": "original",
            "del_worktree.py": "original",
            "mod_master.py": "original",
            "mod_branch.py": "original",
            "mod_both.py": "original",
            "mod_same.py": "original",
            "keep.py": "original",
        },
        commit="Initial commit",
    )
    branch_point = repo.get_hash()
    repo.add(
        {
            "del_master.py": None,
            "add_master.py": "master",
            "mod_master.py": "master",
            "mod_both.py": "master",
            "mod_same.py": "same",
        },
        commit="master",
    )
    repo.create_branch("branch", branch_point)
    repo.add(
        {
            "del_branch.py": None,
            "mod_branch.py": "branch",
            "mod_both.py": "branch",
            "mod_same.py": "same",
        },
        commit="branch",
    )
    repo.add(
        {"del_index.py": None, "add_index.py": "index", "mod_index.py": "index"}
    )
    (repo.root / "del_worktree.py").unlink()
    (repo.root / "add_worktree.py").write_bytes(b"worktree")
    (repo.root / "mod_worktree.py").write_bytes(b"worktree")
    return repo

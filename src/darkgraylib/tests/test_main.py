"""Unit tests for the `darkgraylib.main` module."""

# pylint: disable=too-many-arguments,too-many-positional-arguments,use-dict-literal

from pathlib import Path

import pytest

from darkgraylib.main import resolve_paths


@pytest.mark.kwparametrize(
    dict(
        stdin_filename=".",
        expect_paths={"."},
        expect_root="{cwd}",
    ),
    dict(
        stdin_filename="stdin.py",
        expect_paths={"stdin.py"},
        expect_root="{cwd}",
    ),
    dict(
        stdin_filename="subdir/stdin.py",
        expect_paths={"subdir/stdin.py"},
        expect_root="{cwd}/subdir",
    ),
    dict(
        stdin_filename="subdir/subsubdir/stdin.py",
        expect_paths={"subdir/subsubdir/stdin.py"},
        expect_root="{cwd}/subdir/subsubdir",
    ),
    dict(
        src=["."],
        expect_paths={"."},
        expect_root="{cwd}",
    ),
    dict(
        src=["src1.py", "src2.py"],
        expect_paths={"src1.py", "src2.py"},
        expect_root="{cwd}",
    ),
    dict(
        src=["subdir/src1.py", "subdir/src2.py"],
        expect_paths={"subdir/src1.py", "subdir/src2.py"},
        expect_root="{cwd}/subdir",
    ),
    dict(
        src=["subdir/src1.py", "subdir/src2.py"],
        cwd="subdir",
        expect_paths={"subdir/src1.py", "subdir/src2.py"},
        expect_root="{cwd}/subdir",
    ),
    dict(
        src=["subdir/subsubdir"],
        cwd="subdir",
        expect_paths={"subdir/subsubdir"},
        expect_root="{cwd}/subdir",
    ),
    stdin_filename=None,
    src=[],
    cwd=".",
)
def test_resolve_paths(
    tmp_path, monkeypatch, stdin_filename, src, cwd, expect_paths, expect_root
):
    """Test the `resolve_paths` function"""
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "subsubdir").mkdir()
    monkeypatch.chdir(tmp_path / cwd)

    paths, root = resolve_paths(stdin_filename, src)

    assert paths == {Path(p) for p in expect_paths}
    assert root == Path(expect_root.format(cwd=Path.cwd()))

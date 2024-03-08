from darkgraylib import black_compat


def test_find_project_root(monkeypatch, tmpdir):
    monkeypatch.chdir(tmpdir)
    (tmpdir / "pyproject.toml").write("\n")
    result = black_compat.find_project_root(["test1.py"])
    assert result == tmpdir

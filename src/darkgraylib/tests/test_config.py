"""Tests for `darkgraylib.config`"""

import os
import re
from argparse import ArgumentParser, Namespace
from textwrap import dedent

import pytest
from toml import TomlDecodeError

from darkgraylib.config import (
    ConfigurationError,
    BaseConfig,
    TomlArrayLinesEncoder,
    dump_config,
    get_effective_config,
    get_modified_config,
    load_config,
)
from darkgraylib.testtools.helpers import raises_if_exception

pytestmark = pytest.mark.usefixtures("find_project_root_cache_clear")


@pytest.mark.kwparametrize(
    dict(list_value=[], expect="[\n]"),
    dict(list_value=["one value"], expect='[\n    "one value",\n]'),
    dict(list_value=["two", "values"], expect='[\n    "two",\n    "values",\n]'),
    dict(
        list_value=[
            "a",
            "dozen",
            "short",
            "string",
            "values",
            "in",
            "the",
            "list",
            "of",
            "strings",
            "to",
            "format",
        ],
        expect=(
            '[\n    "a",\n    "dozen",\n    "short",\n    "string",\n    "values"'
            ',\n    "in",\n    "the",\n    "list",\n    "of",\n    "strings"'
            ',\n    "to",\n    "format",\n]'
        ),
    ),
)
def test_toml_array_lines_encoder(list_value, expect):
    """``TomlArrayLinesEncoder`` formats lists with each item on its own line"""
    result = TomlArrayLinesEncoder().dump_list(list_value)

    assert result == expect


class OriginTrackingConfig(BaseConfig):
    """A configuration class that tracks the originating file for the configuration"""

    origin: str


@pytest.mark.kwparametrize(
    dict(),  # pylint: disable=use-dict-literal
    dict(cwd="lvl1"),
    dict(cwd="lvl1/lvl2"),
    dict(cwd="has_git", expect={}),
    dict(cwd="has_git/lvl1", expect={}),
    dict(cwd="has_pyp", expect={"config": "has_pyp"}),
    dict(cwd="has_pyp/lvl1", expect={"config": "has_pyp"}),
    dict(srcs=["root.py"]),
    dict(srcs=["../root.py"], cwd="lvl1"),
    dict(srcs=["../root.py"], cwd="has_git"),
    dict(srcs=["../root.py"], cwd="has_pyp"),
    dict(srcs=["root.py", "lvl1/lvl1.py"]),
    dict(srcs=["../root.py", "lvl1.py"], cwd="lvl1"),
    dict(srcs=["../root.py", "../lvl1/lvl1.py"], cwd="has_git"),
    dict(srcs=["../root.py", "../lvl1/lvl1.py"], cwd="has_pyp"),
    dict(srcs=["has_pyp/pyp.py", "lvl1/lvl1.py"]),
    dict(srcs=["../has_pyp/pyp.py", "lvl1.py"], cwd="lvl1"),
    dict(srcs=["../has_pyp/pyp.py", "../lvl1/lvl1.py"], cwd="has_git"),
    dict(srcs=["pyp.py", "../lvl1/lvl1.py"], cwd="has_pyp"),
    dict(
        srcs=["has_pyp/lvl1/l1.py", "has_pyp/lvl1b/l1b.py"],
        expect={"config": "has_pyp"},
    ),
    dict(
        srcs=["../has_pyp/lvl1/l1.py", "../has_pyp/lvl1b/l1b.py"],
        cwd="lvl1",
        expect={"config": "has_pyp"},
    ),
    dict(
        srcs=["../has_pyp/lvl1/l1.py", "../has_pyp/lvl1b/l1b.py"],
        cwd="has_git",
        expect={"config": "has_pyp"},
    ),
    dict(
        srcs=["lvl1/l1.py", "lvl1b/l1b.py"],
        cwd="has_pyp",
        expect={"config": "has_pyp"},
    ),
    dict(
        srcs=["full_example/full.py"],
        expect={
            "log_level": 'DEBUG',
            "revision": "main",
            "src": ["src", "tests"],
        },
    ),
    dict(srcs=["stdout_example/dummy.py"], expect={"stdout": True}),
    dict(confpath="c", expect={"origin": "c/pyproject.toml"}),
    dict(confpath="c/pyproject.toml", expect={"origin": "c/pyproject.toml"}),
    dict(cwd="lvl1", confpath="../c", expect={"origin": "c/pyproject.toml"}),
    dict(
        cwd="lvl1",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(cwd="lvl1/lvl2", confpath="../../c", expect={"origin": "c/pyproject.toml"}),
    dict(
        cwd="lvl1/lvl2",
        confpath="../../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(cwd="has_git", confpath="../c", expect={"origin": "c/pyproject.toml"}),
    dict(
        cwd="has_git",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(cwd="has_git/lvl1", confpath="../../c", expect={"origin": "c/pyproject.toml"}),
    dict(
        cwd="has_git/lvl1",
        confpath="../../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(cwd="has_pyp", confpath="../c", expect={"origin": "c/pyproject.toml"}),
    dict(
        cwd="has_pyp",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(cwd="has_pyp/lvl1", confpath="../../c", expect={"origin": "c/pyproject.toml"}),
    dict(
        cwd="has_pyp/lvl1",
        confpath="../../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(srcs=["root.py"], confpath="c", expect={"origin": "c/pyproject.toml"}),
    dict(
        srcs=["root.py"],
        confpath="c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py"],
        cwd="lvl1",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py"],
        cwd="lvl1",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py"],
        cwd="has_git",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py"],
        cwd="has_git",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py"],
        cwd="has_pyp",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py"],
        cwd="has_pyp",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["root.py", "lvl1/lvl1.py"],
        confpath="c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["root.py", "lvl1/lvl1.py"],
        confpath="c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py", "lvl1.py"],
        cwd="lvl1",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py", "lvl1.py"],
        cwd="lvl1",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py", "../lvl1/lvl1.py"],
        cwd="has_git",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py", "../lvl1/lvl1.py"],
        cwd="has_git",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py", "../lvl1/lvl1.py"],
        cwd="has_pyp",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../root.py", "../lvl1/lvl1.py"],
        cwd="has_pyp",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["has_pyp/pyp.py", "lvl1/lvl1.py"],
        confpath="c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["has_pyp/pyp.py", "lvl1/lvl1.py"],
        confpath="c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/pyp.py", "lvl1.py"],
        cwd="lvl1",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/pyp.py", "lvl1.py"],
        cwd="lvl1",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/pyp.py", "../lvl1/lvl1.py"],
        cwd="has_git",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/pyp.py", "../lvl1/lvl1.py"],
        cwd="has_git",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["pyp.py", "../lvl1/lvl1.py"],
        cwd="has_pyp",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["pyp.py", "../lvl1/lvl1.py"],
        cwd="has_pyp",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["has_pyp/lvl1/l1.py", "has_pyp/lvl1b/l1b.py"],
        confpath="c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["has_pyp/lvl1/l1.py", "has_pyp/lvl1b/l1b.py"],
        confpath="c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/lvl1/l1.py", "../has_pyp/lvl1b/l1b.py"],
        cwd="lvl1",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/lvl1/l1.py", "../has_pyp/lvl1b/l1b.py"],
        cwd="lvl1",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/lvl1/l1.py", "../has_pyp/lvl1b/l1b.py"],
        cwd="has_git",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["../has_pyp/lvl1/l1.py", "../has_pyp/lvl1b/l1b.py"],
        cwd="has_git",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["lvl1/l1.py", "lvl1b/l1b.py"],
        cwd="has_pyp",
        confpath="../c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["lvl1/l1.py", "lvl1b/l1b.py"],
        cwd="has_pyp",
        confpath="../c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["full_example/full.py"],
        confpath="c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["full_example/full.py"],
        confpath="c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["stdout_example/dummy.py"],
        confpath="c",
        expect={"origin": "c/pyproject.toml"},
    ),
    dict(
        srcs=["stdout_example/dummy.py"],
        confpath="c/pyproject.toml",
        expect={"origin": "c/pyproject.toml"},
    ),
    srcs=[],
    cwd=".",
    confpath=None,
    expect={"config": "no_pyp"},
)
def test_load_config_path(  # pylint: disable=too-many-arguments
    tmp_path, monkeypatch, srcs, cwd, confpath, expect
):
    """``load_config()`` finds and loads configuration based on source file paths"""
    (tmp_path / ".git").mkdir()
    (tmp_path / "pyproject.toml").write_text('[tool.darkgraylib]\nconfig = "no_pyp"\n')
    (tmp_path / "lvl1/lvl2").mkdir(parents=True)
    (tmp_path / "has_git/.git").mkdir(parents=True)
    (tmp_path / "has_git/lvl1").mkdir()
    (tmp_path / "has_pyp/lvl1").mkdir(parents=True)
    (tmp_path / "has_pyp/pyproject.toml").write_text(
        '[tool.darkgraylib]\nconfig = "has_pyp"\n'
    )
    (tmp_path / "full_example").mkdir()
    (tmp_path / "full_example/pyproject.toml").write_text(
        dedent(
            """
            [tool.darkgraylib]
            src = [
                "src",
                "tests",
            ]
            revision = "main"
            log_level = "DEBUG"
            """
        )
    )
    (tmp_path / "stdout_example").mkdir()
    (tmp_path / "stdout_example/pyproject.toml").write_text(
        "[tool.darkgraylib]\nstdout = true\n"
    )
    (tmp_path / "c").mkdir()
    (tmp_path / "c" / "pyproject.toml").write_text(
        "[tool.darkgraylib]\norigin = 'c/pyproject.toml'\n"
    )
    monkeypatch.chdir(tmp_path / cwd)

    result = load_config(confpath, srcs, "darkgraylib", OriginTrackingConfig)

    assert result == expect


@pytest.mark.kwparametrize(
    dict(path=".", expect="Configuration file pyproject.toml not found"),
    dict(path="./foo.toml", expect="Configuration file ./foo.toml not found"),
    dict(
        path="empty", expect=f"Configuration file empty{os.sep}pyproject.toml not found"
    ),
    dict(
        path="empty/",
        expect=f"Configuration file empty{os.sep}pyproject.toml not found",
    ),
    dict(path="subdir/foo.toml", expect="Configuration file subdir/foo.toml not found"),
    dict(
        path="missing_dir",
        expect="Configuration file missing_dir not found",
    ),
    dict(
        path=f"missing_dir{os.sep}",
        expect=f"Configuration file missing_dir{os.sep}pyproject.toml not found",
    ),
    dict(
        path="missing_dir/foo.toml",
        expect="Configuration file missing_dir/foo.toml not found",
    ),
)
def test_load_config_explicit_path_errors(tmp_path, monkeypatch, path, expect):
    """``load_config()`` raises an error if given path is not a file"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "pyproject.toml").write_text("")
    (tmp_path / "empty").mkdir()
    with pytest.raises(ConfigurationError, match=re.escape(expect)):

        _ = load_config(path, ["."], "darkgraylib", BaseConfig)


@pytest.mark.kwparametrize(
    dict(args=Namespace(), expect={}),
    dict(args=Namespace(one="option"), expect={"one": "option"}),
    dict(args=Namespace(log_level=10), expect={"log_level": "DEBUG"}),
    dict(
        args=Namespace(two="options", log_level=20),
        expect={"two": "options", "log_level": "INFO"},
    ),
)
def test_get_effective_config(args, expect):
    """``get_effective_config()`` converts command line options correctly"""
    with raises_if_exception(expect):

        result = get_effective_config(args, BaseConfig)

        assert result == expect


@pytest.mark.kwparametrize(
    dict(args=Namespace(), expect={}),
    dict(args=Namespace(unknown="option"), expect={"unknown": "option"}),
    dict(args=Namespace(log_level=10), expect={"log_level": "DEBUG"}),
    dict(args=Namespace(names=[], int=42, string="fourty-two"), expect={"names": []}),
    dict(
        args=Namespace(names=["bar"], int=42, string="fourty-two"),
        expect={"names": ["bar"]},
    ),
    dict(
        args=Namespace(names=["foo"], int=43, string="fourty-two"), expect={"int": 43}
    ),
    dict(args=Namespace(names=["foo"], int=42, string="one"), expect={"string": "one"}),
)
def test_get_modified_config(args, expect):
    """``get_modified_config()`` only includes non-default configuration options"""
    parser = ArgumentParser()
    parser.add_argument("names", nargs="*", default=["foo"])
    parser.add_argument("--int", dest="int", default=42)
    parser.add_argument("--string", default="fourty-two")

    result = get_modified_config(parser, args, BaseConfig)

    assert result == expect


@pytest.mark.kwparametrize(
    dict(config={}, expect="[tool.darkgraylib]\n"),
    dict(config={"str": "value"}, expect='[tool.darkgraylib]\nstr = "value"\n'),
    dict(config={"int": 42}, expect="[tool.darkgraylib]\nint = 42\n"),
    dict(config={"float": 4.2}, expect="[tool.darkgraylib]\nfloat = 4.2\n"),
    dict(
        config={"list": ["foo", "bar"]},
        expect=dedent(
            """\
            [tool.darkgraylib]
            list = [
                "foo",
                "bar",
            ]
            """
        ),
    ),
    dict(
        config={
            "src": ["main.py"],
            "revision": "master",
            "config": None,
            "log_level": "DEBUG",
        },
        expect=dedent(
            """\
            [tool.darkgraylib]
            src = [
                "main.py",
            ]
            revision = "master"
            log-level = "DEBUG"
            """
        ),
    ),
)
def test_dump_config(config, expect):
    """``dump_config()`` outputs configuration correctly in the TOML format"""
    result = dump_config(config, "darkgraylib")

    assert result == expect


@pytest.mark.parametrize(
    ["config", "expect"],
    [
        ("", {}),
        ("src = []", {"src": []}),
        ("src = ['your.py']", {"src": ["your.py"]}),
        ("revision = 'your-branch'", {"revision": "your-branch"}),
        ("stdout = false", {"stdout": False}),
        ("stdout = true", {"stdout": True}),
        ("stdout = no", TomlDecodeError),
        ("config = 'your.conf'", {"config": "your.conf"}),
        ("log_level = 0", {"log_level": "NOTSET"}),
        ("log_level = 'NOTSET'", {"log_level": "NOTSET"}),
        ("log_level = 1", {"log_level": "Level 1"}),
        ("log_level = 2", {"log_level": "Level 2"}),
        ("log_level = 10", {"log_level": "DEBUG"}),
        ("log_level = 'DEBUG'", {"log_level": "DEBUG"}),
        ("log_level = DEBUG", TomlDecodeError),
        ("log_level = 20", {"log_level": "INFO"}),
        ("log_level = 'INFO'", {"log_level": "INFO"}),
        ("log_level = 30", {"log_level": "WARNING"}),
        ("log_level = 'WARNING'", {"log_level": "WARNING"}),
        ("log_level = 40", {"log_level": "ERROR"}),
        ("log_level = 'ERROR'", {"log_level": "ERROR"}),
        ("log_level = 50", {"log_level": "CRITICAL"}),
        ("log_level = 'CRITICAL'", {"log_level": "CRITICAL"}),
        ("color = false", {"color": False}),
        ("color = true", {"color": True}),
        ("workers = 0", {"workers": 0}),
        ("workers = 1", {"workers": 1}),
        ("workers = 42", {"workers": 42}),
        ("invalid_option = 42", ConfigurationError),
        ("quiet = false", {"quiet": False}),
        ("quiet = true", {"quiet": True}),
    ],
)
def test_load_config(tmp_path, monkeypatch, config, expect):
    """`load_config()` can load all supported options"""
    (tmp_path / "pyproject.toml").write_text(f"[tool.darkgraylib]\n{config}\n")
    monkeypatch.chdir(tmp_path)
    with raises_if_exception(expect):

        result = load_config(None, ["."], "darkgraylib", BaseConfig)

        assert result == expect
        assert {k: type(v) for k, v in result.items()} == {
            k: type(v) for k, v in expect.items()
        }

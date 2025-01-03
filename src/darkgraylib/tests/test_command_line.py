"""Unit tests for `darkgraylib.command_line` and `darkgraylib.main`."""

# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
# pylint: disable=use-dict-literal

import os
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
import toml

from darkgraylib.command_line import make_argument_parser, parse_command_line
from darkgraylib.config import BaseConfig
from darkgraylib.testtools.helpers import filter_dict, raises_if_exception
from darkgraylib.testtools.mock_argument_parser import make_test_argument_parser
from darkgraylib.version import __version__

pytestmark = pytest.mark.usefixtures("find_project_root_cache_clear")


@pytest.mark.parametrize("version", [{}, {"version": "0.123.456"},])
def test_make_argument_parser_version(version, capsys):
    """Test that make_argument_parser sets the correct version."""
    parser = make_argument_parser(
        require_src=True,
        application="TestApp",
        description="Test description",
        config_help="Test config help",
        **version,
    )

    with pytest.raises(SystemExit):
        parser.parse_args(["--version"])

    captured = capsys.readouterr()
    expected_version = version.get("version", __version__)
    assert captured.out.strip() == expected_version


@pytest.mark.parametrize("version", [{}, {"version": "0.123.456"}])
def test_parse_command_line_version(version, capsys):
    """Test that parse_command_line respects the version from the parser factory."""
    def factory(require_src):
        return make_argument_parser(
            require_src=require_src,
            application="TestApp",
            description="Test description",
            config_help="Test config help",
            **version,
        )
    with pytest.raises(SystemExit):
        parse_command_line(
            argument_parser_factory=factory,
            argv=["--version"],
            section_name="test",
            config_type=BaseConfig,
        )

    captured = capsys.readouterr()
    expected_version = version.get("version", __version__)
    assert captured.out.strip() == expected_version


@pytest.mark.kwparametrize(
    dict(config=None, argv=[], expect=SystemExit),
    dict(
        config=None,
        argv=["file.py"],
        expect={"src": ["file.py"]},
    ),
    dict(
        config={"src": ["file.py"]},
        argv=[],
        expect={"src": ["file.py"]},
    ),
    dict(
        config={"src": ["file.py"]},
        argv=["file.py"],
        expect={"src": ["file.py"]},
    ),
    dict(
        config={"src": ["file1.py"]},
        argv=["file2.py"],
        expect={"src": ["file2.py"]},
    ),
)
def test_parse_command_line_config_src(
    tmpdir,
    monkeypatch,
    config,
    argv,
    expect,
):
    """The ``src`` positional argument from config and cmdline is handled correctly"""
    monkeypatch.chdir(tmpdir)
    if config is not None:
        toml.dump({"tool": {"darkgraylib": config}}, tmpdir / "pyproject.toml")
    with raises_if_exception(expect):

        args, effective_cfg, modified_cfg = parse_command_line(
            make_test_argument_parser,
            argv,
            "darkgraylib",
            BaseConfig,
        )

        assert filter_dict(args.__dict__, "src") == expect
        assert filter_dict(dict(effective_cfg), "src") == expect
        assert filter_dict(dict(modified_cfg), "src") == expect


@pytest.mark.kwparametrize(
    dict(argv=["."], expect="root..HEAD"),
    dict(argv=["./subdir/"], expect="subdir..HEAD"),
    dict(argv=["--config", "./pyproject.toml", "."], expect="root..HEAD"),
    dict(argv=["--config", "./subdir/pyproject.toml", "."], expect="subdir..HEAD"),
    dict(argv=["--config", "./pyproject.toml", "subdir/"], expect="root..HEAD"),
    dict(
        argv=["--config", "./subdir/pyproject.toml", "subdir/"], expect="subdir..HEAD"
    ),
)
def test_parse_command_line_config_location_specified(
    tmp_path,
    monkeypatch,
    argv,
    expect,
):
    """Configuration is read from file pointed to using ``-c``/``--config``."""
    monkeypatch.chdir(tmp_path)
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    root_config = tmp_path / "pyproject.toml"
    subdir_config = subdir / "pyproject.toml"
    root_config.write_text(
        toml.dumps({"tool": {"darkgraylib": {"revision": "root..HEAD"}}})
    )
    subdir_config.write_text(
        toml.dumps({"tool": {"darkgraylib": {"revision": "subdir..HEAD"}}})
    )

    args, effective_cfg, modified_cfg = parse_command_line(
        make_test_argument_parser,
        argv,
        "darkgraylib",
        BaseConfig,
    )

    assert args.revision == expect
    assert effective_cfg["revision"] == expect
    assert modified_cfg["revision"] == expect


@pytest.mark.kwparametrize(
    dict(
        argv=["."],
        expect_value=("src", ["."]),
        expect_config=("src", ["."]),
        expect_modified=("src", ["."]),
    ),
    dict(
        argv=["."],
        expect_value=("revision", "HEAD"),
        expect_config=("revision", "HEAD"),
        expect_modified=("revision", ...),
    ),
    dict(
        argv=["-rmaster", "."],
        expect_value=("revision", "master"),
        expect_config=("revision", "master"),
        expect_modified=("revision", "master"),
    ),
    dict(
        argv=["--revision", "HEAD", "."],
        expect_value=("revision", "HEAD"),
        expect_config=("revision", "HEAD"),
        expect_modified=("revision", ...),
    ),
    dict(
        argv=["."],
        expect_value=("config", None),
        expect_config=("config", None),
        expect_modified=("config", ...),
    ),
    dict(
        argv=["-c", "my.cfg", "."],
        expect_value=("config", "my.cfg"),
        expect_config=("config", "my.cfg"),
        expect_modified=("config", "my.cfg"),
    ),
    dict(
        argv=["--config=my.cfg", "."],
        expect_value=("config", "my.cfg"),
        expect_config=("config", "my.cfg"),
        expect_modified=("config", "my.cfg"),
    ),
    dict(
        argv=["-c", "subdir_with_config", "."],
        expect_value=("config", "subdir_with_config"),
        expect_config=("config", "subdir_with_config"),
        expect_modified=("config", "subdir_with_config"),
    ),
    dict(
        argv=["--config=subdir_with_config", "."],
        expect_value=("config", "subdir_with_config"),
        expect_config=("config", "subdir_with_config"),
        expect_modified=("config", "subdir_with_config"),
    ),
    dict(
        argv=["."],
        expect_value=("log_level", 30),
        expect_config=("log_level", "WARNING"),
        expect_modified=("log_level", ...),
    ),
    dict(
        argv=["-v", "."],
        expect_value=("log_level", 20),
        expect_config=("log_level", "INFO"),
        expect_modified=("log_level", "INFO"),
    ),
    dict(
        argv=["--verbose", "-v", "."],
        expect_value=("log_level", 10),
        expect_config=("log_level", "DEBUG"),
        expect_modified=("log_level", "DEBUG"),
    ),
    dict(
        argv=["-q", "."],
        expect_value=("log_level", 40),
        expect_config=("log_level", "ERROR"),
        expect_modified=("log_level", "ERROR"),
    ),
    dict(
        argv=["--quiet", "-q", "."],
        expect_value=("log_level", 50),
        expect_config=("log_level", "CRITICAL"),
        expect_modified=("log_level", "CRITICAL"),
    ),
    dict(
        argv=["."],
        environ={},
        expect_value=("color", None),
        expect_config=("color", None),
        expect_modified=("color", ...),
    ),
    dict(
        argv=["."],
        environ={"PY_COLORS": "0"},
        expect_value=("color", False),
        expect_config=("color", False),
        expect_modified=("color", False),
    ),
    dict(
        argv=["."],
        environ={"PY_COLORS": "1"},
        expect_value=("color", True),
        expect_config=("color", True),
        expect_modified=("color", True),
    ),
    dict(
        argv=["--color", "."],
        environ={},
        expect_value=("color", True),
        expect_config=("color", True),
        expect_modified=("color", True),
    ),
    dict(
        argv=["--color", "."],
        environ={"PY_COLORS": "0"},
        expect_value=("color", True),
        expect_config=("color", True),
        expect_modified=("color", True),
    ),
    dict(
        argv=["--color", "."],
        environ={"PY_COLORS": "1"},
        expect_value=("color", True),
        expect_config=("color", True),
        expect_modified=("color", True),
    ),
    dict(
        argv=["--no-color", "."],
        environ={},
        expect_value=("color", False),
        expect_config=("color", False),
        expect_modified=("color", False),
    ),
    dict(
        argv=["--no-color", "."],
        environ={"PY_COLORS": "0"},
        expect_value=("color", False),
        expect_config=("color", False),
        expect_modified=("color", False),
    ),
    dict(
        argv=["--no-color", "."],
        environ={"PY_COLORS": "1"},
        expect_value=("color", False),
        expect_config=("color", False),
        expect_modified=("color", False),
    ),
    dict(
        # this is accepted as a path, but would later fail if a file or directory with
        # that funky name doesn't exist
        argv=["--suspicious path"],
        expect_value=("src", ["--suspicious path"]),
        expect_config=("src", ["--suspicious path"]),
        expect_modified=("src", ["--suspicious path"]),
    ),
    dict(
        argv=["valid/path", "another/valid/path"],
        expect_value=("src", ["valid/path", "another/valid/path"]),
        expect_config=("src", ["valid/path", "another/valid/path"]),
        expect_modified=("src", ["valid/path", "another/valid/path"]),
    ),
    environ={},
)
def test_parse_command_line(
    tmp_path, monkeypatch, argv, environ, expect_value, expect_config, expect_modified
):
    """``parse_command_line()`` parses options correctly"""
    monkeypatch.chdir(tmp_path)
    (tmp_path / "dummy.py").touch()
    (tmp_path / "my.cfg").touch()
    (tmp_path / "subdir_with_config").mkdir()
    (tmp_path / "subdir_with_config" / "pyproject.toml").touch()
    with patch.dict(os.environ, environ, clear=True), raises_if_exception(
        expect_value
    ) as expect_exception:
        args, effective_cfg, modified_cfg = parse_command_line(
            make_test_argument_parser, argv, "darkgraylib", BaseConfig
        )

    if not expect_exception:
        arg_name, expect_arg_value = expect_value
        assert getattr(args, arg_name) == expect_arg_value

        option, expect_config_value = expect_config
        if expect_config_value is ...:
            assert option not in effective_cfg
        else:
            assert effective_cfg[option] == expect_config_value  # type: ignore

        modified_option, expect_modified_value = expect_modified
        if expect_modified_value is ...:
            assert modified_option not in modified_cfg
        else:
            assert (
                modified_cfg[modified_option] == expect_modified_value  # type: ignore
            )


def test_parse_command_line_load_config_hook_called(tmp_path, monkeypatch):
    """The load configuration hook is called correctly."""
    monkeypatch.chdir(tmp_path)
    with Path("pyproject.toml").open("w", encoding="utf-8") as pyproject:
        toml.dump({"tool": {"darkgraylib": {"revision": "main"}}}, pyproject)
    hook_mock = Mock()

    parse_command_line(
        make_test_argument_parser, ["x.py"], "darkgraylib", BaseConfig, hook_mock,
    )

    hook_mock.assert_called_once_with({"revision": "main"})


def test_parse_command_line_invalid_arguments(capsys):
    """Test that parse_command_line exits with code 3 for invalid arguments."""
    with pytest.raises(SystemExit) as excinfo:
        parse_command_line(
            make_test_argument_parser, ["--invalid-option"], "darkgraylib", BaseConfig
        )

    assert excinfo.value.code == 3
    captured = capsys.readouterr()
    assert "error: unrecognized arguments: --invalid-option" in captured.err

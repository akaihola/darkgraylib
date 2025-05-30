"""Unit tests for `darkgraylib.utils`."""

# pylint: disable=redefined-outer-name,use-dict-literal

import os
from pathlib import Path

import pytest

from darkgraylib.utils import (
    TextDocument,
    detect_newline,
    get_common_root,
    get_path_ancestry,
    joinlines,
)


@pytest.fixture(params=[TextDocument.from_file, TextDocument.from_bytes])
def textdocument_factory(request):
    """Fixture for a factory function that creates a ``TextDocument``

    The fixture can be parametrized with `(bytes) -> TextDocument` functions
    that take the raw bytes of the document.

    By default, it is parametrized with the ``TextDocument.from_file()`` (for
    which it creates a temporary file) and the ``TextDocument.from_bytes()``
    classmethods.
    """
    # pylint: disable=comparison-with-callable
    if request.param == TextDocument.from_file:

        def factory(content):
            tmp_path = request.getfixturevalue("tmp_path")
            path = tmp_path / "test.py"
            path.write_bytes(content)
            return TextDocument.from_file(path)

        return factory

    return request.param


@pytest.fixture
def textdocument(request, textdocument_factory):
    """Fixture for a ``TextDocument``

    The fixture must be parametrized with the raw bytes of the document.
    """
    return textdocument_factory(request.param)


@pytest.mark.kwparametrize(
    dict(string="", expect="\n"),
    dict(string="\n", expect="\n"),
    dict(string="\r\n", expect="\r\n"),
    dict(string="one line\n", expect="\n"),
    dict(string="one line\r\n", expect="\r\n"),
    dict(string="first line\nsecond line\n", expect="\n"),
    dict(string="first line\r\nsecond line\r\n", expect="\r\n"),
    dict(string="first unix\nthen windows\r\n", expect="\n"),
    dict(string="first windows\r\nthen unix\n", expect="\r\n"),
)
def test_detect_newline(string, expect):
    """``detect_newline()`` gives correct results"""
    result = detect_newline(string)

    assert result == expect


@pytest.mark.kwparametrize(
    dict(textdocument=TextDocument(), expect="utf-8"),
    dict(textdocument=TextDocument(encoding="utf-8"), expect="utf-8"),
    dict(textdocument=TextDocument(encoding="utf-16"), expect="utf-16"),
    dict(textdocument=TextDocument.from_str(""), expect="utf-8"),
    dict(textdocument=TextDocument.from_str("", encoding="utf-8"), expect="utf-8"),
    dict(textdocument=TextDocument.from_str("", encoding="utf-16"), expect="utf-16"),
    dict(textdocument=TextDocument.from_lines([]), expect="utf-8"),
    dict(textdocument=TextDocument.from_lines([], encoding="utf-8"), expect="utf-8"),
    dict(textdocument=TextDocument.from_lines([], encoding="utf-16"), expect="utf-16"),
)
def test_textdocument_set_encoding(textdocument, expect):
    """TextDocument.encoding is correct from each constructor"""
    assert textdocument.encoding == expect


@pytest.mark.kwparametrize(
    dict(doc=TextDocument(), expect=""),
    dict(doc=TextDocument(lines=["zéro", "un"]), expect="zéro\nun\n"),
    dict(doc=TextDocument(lines=["zéro", "un"], newline="\n"), expect="zéro\nun\n"),
    dict(
        doc=TextDocument(lines=["zéro", "un"], newline="\r\n"), expect="zéro\r\nun\r\n"
    ),
)
def test_textdocument_string(doc, expect):
    """TextDocument.string respects the newline setting"""
    assert doc.string == expect


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.kwparametrize(
    dict(textdocument=TextDocument(), expect=""),
    dict(textdocument=TextDocument(lines=["zéro", "un"])),
    dict(textdocument=TextDocument(string="zéro\nun\n")),
    dict(textdocument=TextDocument(lines=["zéro", "un"], newline="\n")),
    dict(textdocument=TextDocument(string="zéro\nun\n", newline="\n")),
    dict(textdocument=TextDocument(lines=["zéro", "un"], newline="\r\n")),
    dict(textdocument=TextDocument(string="zéro\r\nun\r\n", newline="\r\n")),
    expect="zéro{newline}un{newline}",
)
def test_textdocument_string_with_newline(textdocument, newline, expect):
    """TextDocument.string respects the newline setting"""
    result = textdocument.string_with_newline(newline)

    expected = expect.format(newline=newline)
    assert result == expected


@pytest.mark.kwparametrize(
    dict(encoding="utf-8", newline="\n", expect=b"z\xc3\xa9ro\nun\n"),
    dict(encoding="iso-8859-1", newline="\n", expect=b"z\xe9ro\nun\n"),
    dict(encoding="utf-8", newline="\r\n", expect=b"z\xc3\xa9ro\r\nun\r\n"),
    dict(encoding="iso-8859-1", newline="\r\n", expect=b"z\xe9ro\r\nun\r\n"),
)
def test_textdocument_encoded_string(encoding, newline, expect):
    """TextDocument.encoded_string uses correct encoding and newline"""
    textdocument = TextDocument(
        lines=["zéro", "un"], encoding=encoding, newline=newline
    )

    assert textdocument.encoded_string == expect


@pytest.mark.kwparametrize(
    dict(doc=TextDocument(), expect=()),
    dict(doc=TextDocument(string="zéro\nun\n"), expect=("zéro", "un")),
    dict(doc=TextDocument(string="zéro\nun\n", newline="\n"), expect=("zéro", "un")),
    dict(
        doc=TextDocument(string="zéro\r\nun\r\n", newline="\r\n"), expect=("zéro", "un")
    ),
    dict(
        doc=TextDocument(
            string="# coding: iso-8859-5\n# б\x85б\x86\n", encoding="iso-8859-5"
        ),
        expect=("# coding: iso-8859-5", "# б\x85б\x86"),
    ),
)
def test_textdocument_lines(doc, expect):
    """TextDocument.lines is correct after parsing a string with different newlines"""
    assert doc.lines == expect


@pytest.mark.kwparametrize(
    dict(
        textdocument=TextDocument.from_str(""),
        expect_lines=(),
        expect_encoding="utf-8",
        expect_newline="\n",
        expect_mtime="",
    ),
    dict(
        textdocument=TextDocument.from_str("", encoding="utf-8"),
        expect_lines=(),
        expect_encoding="utf-8",
        expect_newline="\n",
        expect_mtime="",
    ),
    dict(
        textdocument=TextDocument.from_str("", encoding="iso-8859-1"),
        expect_lines=(),
        expect_encoding="iso-8859-1",
        expect_newline="\n",
        expect_mtime="",
    ),
    dict(
        textdocument=TextDocument.from_str("a\nb\n"),
        expect_lines=("a", "b"),
        expect_encoding="utf-8",
        expect_newline="\n",
        expect_mtime="",
    ),
    dict(
        textdocument=TextDocument.from_str("a\r\nb\r\n"),
        expect_lines=("a", "b"),
        expect_encoding="utf-8",
        expect_newline="\r\n",
        expect_mtime="",
    ),
    dict(
        textdocument=TextDocument.from_str("", mtime="my mtime"),
        expect_lines=(),
        expect_encoding="utf-8",
        expect_newline="\n",
        expect_mtime="my mtime",
    ),
)
def test_textdocument_from_str(
    textdocument, expect_lines, expect_encoding, expect_newline, expect_mtime
):
    """TextDocument.from_str() gets correct content, encoding, newlines and mtime"""
    assert textdocument.lines == expect_lines
    assert textdocument.encoding == expect_encoding
    assert textdocument.newline == expect_newline
    assert textdocument.mtime == expect_mtime


@pytest.mark.kwparametrize(
    dict(textdocument=b'print("touch\xc3\xa9")\n', expect="utf-8"),
    dict(textdocument=b'\xef\xbb\xbfprint("touch\xc3\xa9")\n', expect="utf-8-sig"),
    dict(textdocument=b'# coding: iso-8859-1\n"touch\xe9"\n', expect="iso-8859-1"),
    indirect=["textdocument"],
)
def test_textdocument_detect_encoding(textdocument, expect):
    """TextDocument.from_file/bytes() detects the file encoding correctly"""
    assert textdocument.encoding == expect


@pytest.mark.kwparametrize(
    dict(textdocument=b'print("unix")\n', expect="\n"),
    dict(textdocument=b'print("windows")\r\n', expect="\r\n"),
    indirect=["textdocument"],
)
def test_textdocument_detect_newline(textdocument, expect):
    """TextDocument.from_file/bytes() detects the newline sequence correctly"""
    assert textdocument.newline == expect


@pytest.mark.kwparametrize(
    dict(doc1=TextDocument(lines=["foo"]), doc2=TextDocument(lines=[]), expect=False),
    dict(doc1=TextDocument(lines=[]), doc2=TextDocument(lines=["foo"]), expect=False),
    dict(
        doc1=TextDocument(lines=["foo"]), doc2=TextDocument(lines=["bar"]), expect=False
    ),
    dict(
        doc1=TextDocument(lines=["line1", "line2"]),
        doc2=TextDocument(lines=["line1", "line2"]),
        expect=True,
    ),
    dict(
        doc1=TextDocument(lines=["line1", "line2"], encoding="utf-16", newline="\r\n"),
        doc2=TextDocument(lines=["line1", "line2"]),
        expect=True,
    ),
    dict(doc1=TextDocument(lines=["foo"]), doc2=TextDocument(""), expect=False),
    dict(doc1=TextDocument(lines=[]), doc2=TextDocument("foo\n"), expect=False),
    dict(doc1=TextDocument(lines=["foo"]), doc2=TextDocument("bar\n"), expect=False),
    dict(
        doc1=TextDocument(lines=["line1", "line2"]),
        doc2=TextDocument("line1\nline2\n"),
        expect=True,
    ),
    dict(doc1=TextDocument("foo\n"), doc2=TextDocument(lines=[]), expect=False),
    dict(doc1=TextDocument(""), doc2=TextDocument(lines=["foo"]), expect=False),
    dict(doc1=TextDocument("foo\n"), doc2=TextDocument(lines=["bar"]), expect=False),
    dict(
        doc1=TextDocument("line1\nline2\n"),
        doc2=TextDocument(lines=["line1", "line2"]),
        expect=True,
    ),
    dict(doc1=TextDocument("foo\n"), doc2=TextDocument(""), expect=False),
    dict(doc1=TextDocument(""), doc2=TextDocument("foo\n"), expect=False),
    dict(doc1=TextDocument("foo\n"), doc2=TextDocument("bar\n"), expect=False),
    dict(
        doc1=TextDocument("line1\nline2\n"),
        doc2=TextDocument("line1\nline2\n"),
        expect=True,
    ),
    dict(
        doc1=TextDocument("line1\r\nline2\r\n"),
        doc2=TextDocument("line1\nline2\n"),
        expect=True,
    ),
    dict(doc1=TextDocument("foo"), doc2="line1\nline2\n", expect=NotImplemented),
)
def test_textdocument_eq(doc1, doc2, expect):
    """TextDocument.__eq__()"""
    result = doc1.__eq__(doc2)  # pylint: disable=unnecessary-dunder-call

    assert result == expect


@pytest.mark.kwparametrize(
    dict(document=TextDocument(""), expect="TextDocument([0 lines])"),
    dict(document=TextDocument(lines=[]), expect="TextDocument([0 lines])"),
    dict(document=TextDocument("One line\n"), expect="TextDocument([1 lines])"),
    dict(document=TextDocument(lines=["One line"]), expect="TextDocument([1 lines])"),
    dict(document=TextDocument("Two\nlines\n"), expect="TextDocument([2 lines])"),
    dict(
        document=TextDocument(lines=["Two", "lines"]), expect="TextDocument([2 lines])"
    ),
    dict(
        document=TextDocument(mtime="some mtime"),
        expect="TextDocument([0 lines], mtime='some mtime')",
    ),
    dict(
        document=TextDocument(encoding="utf-8"),
        expect="TextDocument([0 lines])",
    ),
    dict(
        document=TextDocument(encoding="a non-default encoding"),
        expect="TextDocument([0 lines], encoding='a non-default encoding')",
    ),
    dict(
        document=TextDocument(newline="\n"),
        expect="TextDocument([0 lines])",
    ),
    dict(
        document=TextDocument(newline="a non-default newline"),
        expect="TextDocument([0 lines], newline='a non-default newline')",
    ),
)
def test_textdocument_repr(document, expect):
    """TextDocument.__repr__()"""
    result = repr(document)

    assert result == expect


@pytest.mark.kwparametrize(
    dict(document=TextDocument(), expect=""),
    dict(document=TextDocument(mtime=""), expect=""),
    dict(document=TextDocument(mtime="dummy mtime"), expect="dummy mtime"),
)
def test_textdocument_mtime(document, expect):
    """TextDocument.mtime"""
    assert document.mtime == expect


def test_textdocument_from_file(tmp_path):
    """TextDocument.from_file()"""
    dummy_txt = tmp_path / "dummy.txt"
    dummy_txt.write_bytes(b"# coding: iso-8859-1\r\ndummy\r\ncontent\r\n")
    os.utime(dummy_txt, (1_000_000_000, 1_000_000_000))

    document = TextDocument.from_file(dummy_txt)

    assert document.string == "# coding: iso-8859-1\r\ndummy\r\ncontent\r\n"
    assert document.lines == ("# coding: iso-8859-1", "dummy", "content")
    assert document.encoding == "iso-8859-1"
    assert document.newline == "\r\n"
    assert document.mtime == "2001-09-09 01:46:40.000000 +0000"


def test_joinlines():
    """``joinlines() concatenates and adds a newline after each given string item"""
    result = joinlines(("a", "b", "c"))
    assert result == "a\nb\nc\n"


def test_get_common_root_empty():
    """``get_common_root()`` raises a ``ValueError`` if ``paths`` argument is empty"""
    with pytest.raises(ValueError):
        get_common_root([])


def test_get_common_root(tmpdir):
    """``get_common_root()`` traverses backwards correctly"""
    tmpdir = Path(tmpdir)
    path1 = tmpdir / "a" / "b" / "c" / "d"
    path2 = tmpdir / "a" / "e" / ".." / "b" / "f" / "g"
    path3 = tmpdir / "a" / "h" / ".." / "b" / "i"
    result = get_common_root([path1, path2, path3])
    assert result == tmpdir / "a" / "b"


def test_get_common_root_of_directory(tmpdir):
    """``get_common_root()`` returns a single directory itself"""
    tmpdir = Path(tmpdir)
    result = get_common_root([tmpdir])
    assert result == tmpdir


def test_get_path_ancestry_for_directory(tmpdir):
    """``get_path_ancestry()`` includes a directory itself as the last item"""
    tmpdir = Path(tmpdir)
    result = list(get_path_ancestry(tmpdir))
    assert result[-1] == tmpdir
    assert result[-2] == tmpdir.parent


def test_get_path_ancestry_for_file(tmpdir):
    """``get_path_ancestry()`` includes a file's parent directory as the last item"""
    tmpdir = Path(tmpdir)
    dummy = tmpdir / "dummy"
    dummy.write_text("dummy")
    result = list(get_path_ancestry(dummy))
    assert result[-1] == tmpdir
    assert result[-2] == tmpdir.parent

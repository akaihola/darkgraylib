"""Miscellaneous utility functions"""

import io
import sys
import tokenize
from datetime import datetime, timezone
from itertools import chain
from pathlib import Path
from typing import Iterable, Tuple

TextLines = Tuple[str, ...]

WINDOWS = sys.platform.startswith("win")
GIT_DATEFORMAT = "%Y-%m-%d %H:%M:%S.%f +0000"


def detect_newline(string: str) -> str:
    """Detect LF or CRLF newlines in a string by looking at the end of the first line"""
    first_lf_pos = string.find("\n")
    if first_lf_pos > 0 and string[first_lf_pos - 1] == "\r":
        return "\r\n"
    return "\n"


class TextDocument:
    """Store & handle a multi-line text document, either as a string or list of lines"""

    DEFAULT_ENCODING = "utf-8"
    DEFAULT_NEWLINE = "\n"

    def __init__(  # pylint: disable=too-many-arguments
        self,
        string: str = None,
        lines: Iterable[str] = None,
        encoding: str = DEFAULT_ENCODING,
        newline: str = DEFAULT_NEWLINE,
        mtime: str = "",
    ):
        self._string = string
        self._lines = None if lines is None else tuple(lines)
        self._encoding = encoding
        self._newline = newline
        self._mtime = mtime

    def string_with_newline(self, newline: str) -> str:
        """Return the document as a string, using the given newline sequence"""
        if self._string is None or detect_newline(self._string) != newline:
            return joinlines(self.lines or (), newline)
        return self._string

    @property
    def string(self) -> str:
        """Return the document as a string, converting and caching if necessary"""
        if self._string is None:
            self._string = self.string_with_newline(self.newline)
        return self._string

    @property
    def encoded_string(self) -> bytes:
        """Return the document as a bytestring, converting and caching if necessary"""
        return self.string.encode(self.encoding)

    @property
    def lines(self) -> TextLines:
        """Return the document as a list of lines converting and caching if necessary"""
        if self._lines is None:
            self._lines = tuple((self._string or "").splitlines())
        return self._lines

    @property
    def encoding(self) -> str:
        """Return the encoding used in the document"""
        return self._encoding

    @property
    def newline(self) -> str:
        """Return the newline character sequence used in the document"""
        return self._newline

    @property
    def mtime(self) -> str:
        """Return the last modification time of the document"""
        return self._mtime

    @classmethod
    def from_str(
        cls,
        string: str,
        encoding: str = DEFAULT_ENCODING,
        override_newline: str = None,
        mtime: str = "",
    ) -> "TextDocument":
        """Create a document object from a string

        :param string: The contents of the new text document
        :param encoding: The character encoding to be used when writing out the bytes
        :param override_newline: Replace existing newlines with the given newline string
        :param mtime: The modification time of the original file

        """
        newline = detect_newline(string)
        if override_newline and override_newline != newline:
            string = string.replace(newline, override_newline)
            newline = override_newline
        return cls(string, None, encoding=encoding, newline=newline, mtime=mtime)

    @classmethod
    def from_bytes(cls, data: bytes, mtime: str = "") -> "TextDocument":
        """Create a document object from a binary string

        :param data: The binary content of the new text document
        :param mtime: The modification time of the original file

        """
        srcbuf = io.BytesIO(data)
        encoding, lines = tokenize.detect_encoding(srcbuf.readline)
        if not lines:
            return cls(lines=[], encoding=encoding, mtime=mtime)
        return cls.from_str(data.decode(encoding), encoding=encoding, mtime=mtime)

    @classmethod
    def from_file(cls, path: Path) -> "TextDocument":
        """Create a document object by reading a text file

        Also store the last modification time of the file.

        """
        mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).strftime(
            GIT_DATEFORMAT
        )
        with path.open("rb") as srcbuf:
            return cls.from_bytes(srcbuf.read(), mtime)

    @classmethod
    def from_lines(
        cls,
        lines: Iterable[str],
        encoding: str = DEFAULT_ENCODING,
        newline: str = DEFAULT_NEWLINE,
        mtime: str = "",
    ) -> "TextDocument":
        """Create a document object from a list of lines

        The lines should be strings without trailing newlines. They should be encoded in
        UTF-8 unless a different encoding is specified with the ``encoding`` argument.

        """
        return cls(None, lines, encoding=encoding, newline=newline, mtime=mtime)

    def __eq__(self, other: object) -> bool:
        """Compare the equality two text documents, ignoring the modification times"""
        if not isinstance(other, TextDocument):
            return NotImplemented
        if not self._string and not self._lines:
            return not other._string and not other._lines
        return self.lines == other.lines

    def __repr__(self) -> str:
        """Return a Python representation of the document object"""
        encoding = (
            ""
            if self._encoding == self.DEFAULT_ENCODING
            else f", encoding={self.encoding!r}"
        )
        newline = (
            ""
            if self.newline == self.DEFAULT_NEWLINE
            else f", newline={self.newline!r}"
        )
        mtime = "" if not self._mtime else f", mtime={self._mtime!r}"
        return (
            f"{type(self).__name__}("
            f"[{len(self.lines)} lines]"
            f"{encoding}{newline}{mtime})"
        )


DiffChunk = Tuple[int, TextLines, TextLines]


def joinlines(lines: Iterable[str], newline: str = "\n") -> str:
    """Join a list of lines back, adding a linefeed after each line

    This is the reverse of ``str.splitlines()``.

    """
    return "".join(f"{line}{newline}" for line in lines)


def get_path_ancestry(path: Path) -> Iterable[Path]:
    """Return paths to directories leading to the given path

    :param path: The directory or file to get ancestor directories for
    :return: A list of paths, starting from filesystem root and ending in the given
             path (if it's a directory) or the parent of the given path (if it's a file)

    """
    reverse_parents = reversed(path.parents)
    if path.is_dir():
        return chain(reverse_parents, [path])
    return reverse_parents


def get_common_root(paths: Iterable[Path]) -> Path:
    """Find the deepest common parent directory of given paths"""
    resolved_paths = [path.resolve() for path in paths]
    parents = reversed(list(zip(*(get_path_ancestry(path) for path in resolved_paths))))
    for first_path, *other_paths in parents:
        if all(path == first_path for path in other_paths):
            return first_path
    raise ValueError(f"Paths have no common parent Git root: {resolved_paths}")

"""Helper functions for unit tests"""

import re
from contextlib import contextmanager, nullcontext
from typing import Any, Callable, ContextManager, Dict, Iterator, Sequence, Union

import pytest
from _pytest.python_api import RaisesContext


def matching_attrs(obj: BaseException, attrs: Sequence[str]) -> Dict[str, int]:
    """Return object attributes whose name matches one in the given list"""
    return {attname: getattr(obj, attname) for attname in dir(obj) if attname in attrs}


@contextmanager
def raises_or_matches(  # type: ignore[misc]
    expect: Any, match_exc_attrs: Sequence[str]
) -> Iterator[Callable[[Any], bool]]:
    """Helper for matching an expected value or an expected raised exception.

    Examples::

    >>> with raises_or_matches(ValueError("msg"), ["args"]) as check_:
    ...     check_(int("foo"))
    Traceback (most recent call last):
    AssertionError: assert {'args': ("in... 10: 'foo'",)} == {'args': ('msg',)}
      Differing items:
      {'args': ("invalid literal for int() with base 10: 'foo'",)} != {'args': ('msg',)}
      Use -v to get the full diff

    >>> m = "invalid literal for int() with base 10: 'foo'"
    >>> with raises_or_matches(ValueError(m), ["args"]) as check_:
    ...     check_(int("foo"))

    >>> m = "invalid literal for int() with base 10: 'foo'"
    >>> with raises_or_matches(42, []) as check_:
    ...     check_(6 * 7)
    True

    >>> m = "invalid literal for int() with base 10: 'foo'"
    >>> with raises_or_matches(42, []) as check_:
    ...     check_(6 * 8)
    Traceback (most recent call last):
    AssertionError: assert 48 == 42

    :param expect: The expected value or exception
    :param match_exc_attrs: The attributes to match in the expected exception
    :return: A context manager yielding a callback to check the result

    """
    if isinstance(expect, BaseException):
        with pytest.raises(type(expect)) as exc_info:
            # The lambda callback should never get called
            yield lambda result: False
        exception_attributes = matching_attrs(exc_info.value, match_exc_attrs)
        expected_attributes = matching_attrs(expect, match_exc_attrs)
        assert exception_attributes == expected_attributes
    else:

        def check(result: Any) -> bool:
            """Check if the result matches the expected value.

            :param result: The result to check against the expected value
            :raises AssertionError: If the result does not match the expected value

            """
            assert result == expect
            return True

        yield check


def filter_dict(dct: Dict[str, Any], filter_key: str) -> Dict[str, Any]:
    """Return only given keys with their values from a dictionary"""
    return {key: value for key, value in dct.items() if key == filter_key}


def raises_if_exception(expect: Any) -> Union[RaisesContext[Any], ContextManager[None]]:
    """Return a ``pytest.raises`` context manager only if expecting an exception

    If the expected value is not an exception, return a dummy context manager.

    """
    if (isinstance(expect, type) and issubclass(expect, BaseException)) or (
        isinstance(expect, tuple)
        and all(
            isinstance(item, type) and issubclass(item, BaseException)
            for item in expect
        )
    ):
        return pytest.raises(expect)
    if isinstance(expect, BaseException):
        return pytest.raises(type(expect), match=re.escape(str(expect)))
    return nullcontext()

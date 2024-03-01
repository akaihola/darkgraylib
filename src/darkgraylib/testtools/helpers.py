"""Helper functions for unit tests"""

import re
from contextlib import nullcontext
from typing import Any, ContextManager, Dict, Union

import pytest
from _pytest.python_api import RaisesContext


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

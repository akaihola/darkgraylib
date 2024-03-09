"""Configuration and fixtures for the Pytest based test suite"""

import pytest
from darkgraylib.files import find_project_root


@pytest.fixture
def find_project_root_cache_clear() -> None:
    """Clear LRU caching in `darkgraylib.files.find_project_root` before each test.

    To use this on all test cases in a test module, add this to the top::

        pytestmark = pytest.mark.usefixtures("find_project_root_cache_clear")

    NOTE: We use our own copy of the original `black.files.find_project_root` function
    to protect from features and changes not applicable to Darker and Graylint.

    """
    find_project_root.cache_clear()

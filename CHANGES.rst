Unreleased_
===========

These features will be included in the next release:

Added
-----

Fixed
-----

Internal
--------
- Switch from old defunct Bandit action to ``brunohaf/action-bandit``.
- Update Nix action to v31 – fixes the build error.
- Use Safety GitHub action and configure Safety according to its documentation.
- ``--config=check-darkgraylib.toml`` can now be used with ``darker`` to run
  ``ruff format`` and ``isort``, and with ``graylint`` to run Flake8, Mypy,
  Pydocstyle, Pylint and ``ruff check`` on modified parts of Darkgraylib code.
- Provide minimum versions for all dependencies in ``pyproject.toml``.
- Update Pygments to address two CVEs reported by Safety.
- Run baseline Mypy in the CI build using Graylint.


2.4.0_ - 2025-06-10
===================

Fixed
-----
- Make test helper compatible with Pytest_ 8.4+.

Internal
--------
- Use uv_ to test compatibility with future dependency versions.


2.3.0_ - 2025-05-25
===================

Added
-----
- Helpers for handling setuptools entry point plugins.

Internal
-------
- Switch to pyproject.toml_ for project definition, from setup.cfg_.
- Prefer uv_ as the package management tool for the codebase and CI workflows.
- Remove `constraints-oldest.txt` in favor of uv's `--resolution lowest-direct`
  `resolution strategy`_
- For development tools, use `dependency groups`_ instead of extras.
- Update development setup guide in contributing documentation.
- Use consistent Python 3.9+ tooling across all configurations.
- Add `run-lint.sh` and `run-tests.sh` scripts for quick linting and running tests.
- Don't lint the `release_tools` directory.
- Remove obsolete ANN101_ rule from ruff configuration.


2.2.0_ - 2025-01-07
===================

Added
-----
- Add support for Python 3.13.
- Test on development version of Python 3.14.

Removed
-------
- Drop support for Python 3.8.

Fixed
-----
- Only split input files at Python's universal newlines (LF, CRLF, CR), not on more
  exotic newline sequences. This fixes some edge cases in Darker.

Internal
--------
- Update to Pylint 3.3.0+ and adjust disabled messages accordingly.


2.1.0_ - 2024-11-19
===================

Fixed
-----
- Don't convert ``log_level = "<string>"`` in the configuration file to an integer.
- Add the ``quiet = <bool>`` configuration file option.

Internal
--------
- Tools for easy creation of differently scoped Git repository fixtures for tests.
  Helps speed up parameterized tests that need a Git repository, especially on Windows
  where Git process forks are comically expensive. The ``test_git.py`` test module now
  makes use of this and runs in 9s instead of 18s on one Windows laptop.
- Unit tests of configuration file options for `darkgraylib.config.load_config`.
- Keep Pylint below version 3.3.0 until we drop support for Python 3.8.


2.0.1_ - 2024-08-09
===================

Fixed
-----
- When running Git with a clean environment, keep all environment variables and just
  override the language.


2.0.0_ - 2024-07-31
===================

Added
-----
- Return exit code 3 if command line parsing fails. We want to reserve 2 for file not
  found errors which will make GitHub actions easier. Also define constants for various
  exit codes to be used in Darkgraylib and applications which use it.


1.3.2_ - 2024-07-29
===================

Internal
--------
- Added typing to ``diff`` test helpers to solve Mypy errors in Darker.


1.3.1_ - 2024-07-29
===================

Fixed
-----
- Drop the use of ``click``.


1.3.0_ - 2024-07-29
===================

Added
-----
- Make the section name argument for the config dump function mandatory.

Removed
-------
- The config dump section name is now required and is not inferred from the caller.

Fixed
-----
- The `~darkgraylib.command_line.make_argument_parser` function now has a ``version``
  argument which defaults to Darkgraylib's own version. This allows Darker and Graylint
  to correctly report their own version when called with the ``--version`` option.

Internal
--------
- The command ``graylint --config=check-darkgraylib.toml`` now runs Flake8_, Mypy_,
  pydocstyle_, Pylint_ and Ruff_ on modified lines in Python files. Those tools are
  included in the ``[test]`` extra.
- Update ``darkgray-dev-tools`` for Pip >= 24.1 compatibility.


1.2.1_ - 2024-04-21
===================

Added
-----
- Icons in the contributors table in ``README.rst`` now link to searches across both
  Darker and Darkgraylib.

Fixed
-----
- The ``darker -vv`` and ``graylint -vv`` verbosity options now show the correct section
  name ``[tool.darker]`` and ``[tool.graylint]`` in the configuration dump.


1.2.0_ - 2024-04-01
===================

Added
-----
- An optional hook to be called after loading the configuration file. Used by Darker to
  show deprecation warnings for configuration options.

Internal
--------
- The ``release_tools/update_contributors.py`` script was moved to the
  ``darkgray-dev-tools`` repository.
- Badge links in the README on GitHub.
- Replace calls to the deprecated `datetime.datetime.utcfromtimestamp` method with
  `datetime.datetime.fromtimestamp`, passing it the timezone `datetime.timezone.utc`.


1.1.1_ - 2024-03-27
===================

Added
-----
- Support for Python 3.12 in the package metadata and the CI build.

Removed
-------
- Dependency on Black, flynt, isort and regex.

Fixed
-----
- In the ``--update-readme`` command, escape pipe symbols (``|``) in the help output
  placed in the ``README.rst`` file.

Internal
--------
- Run unit tests with the newest Black release, not a fixed version.
- In the future test, upgrade ``toml`` and ``Pygments`` to repository ``master``.
- Messages from future test are now generic, not Black-specific.
- Require ``click`` when running tests.
- Obsolete Mypy configuration options.
- Skip tests on Python 3.13-dev in Windows and macOS. C extension builds are failing,
  this exclusion is to be removed when Python 3.13 has been removed.


1.1.0_ - 2024-03-15
===================

Added
-----
- Rename method on ``git_repo`` plugin to rename/move files in repo.
- Update to Black 24.2.x and isort 5.13.x in pre-commit configuration.

Removed
-------
- ``bump_version.py`` is now in the separate ``darkgray-dev-tools`` repository.

Fixed
-----
- Install ``darkgray-dev-tools`` from PyPI. They don't allow dependencies from GitHub.


1.0.0_ - 2024-03-09
===================

Added
-----
- Copy the code base from Darker 1.7.0.
- Make command line and configuration tooling flexible to provide base command line and
  configuration parsing and common options, allowing these to be used and extended by
  Darker and Graylint.
- Provide ``git_repo`` as a Pytest plugin.
- Configure the ``ruff`` linting tool.
- ``--update-readme`` and ``--verify-readme`` command line options to assist in updating
  and verifying ``--help`` output in the ``README.rst`` file in Darker and Graylint.
- Drop support for Python 3.7.
- Limit Black to versions before 24.2 until the incompatibility is resolved or Black
  requirement removed.
- Allow ``-`` as the single source filename when using the ``--stdin-filename`` option.
  This makes the option compatible with Black.
- Upgrade NixOS tests to use Python 3.11 on both Linux and macOS.

Removed
-------
- Remove the Darker GitHub action.
- No CI test needed for ``--help`` output.
- Reformatting logic and command line moved to Darker.
- Linting support moved to Graylint.
- Handling of Darker and Graylint specific command line options and configuration moved
  to the respective packages.

Fixed
-----
- Rename the package to ``darkgraylib``.
- Update imports and configure ``setuptools``, release tools, linters, issue report
  templates, and CI workflows for the new package name.
- Rename ``darkgraylib.__main__`` to ``.main``.
- Use ``git worktree`` instead of ``git clone`` and ``git checkout`` to set up a
  temporary working tree for running linters for a baseline in the ``rev1`` revision of
  the repository.
- Include the ``py.typed`` typing marker in distributions.
- Python 3.12 compatibility in multi-line string scanning.
- Upgrade ``install-nix-action`` to version 22 in CI to fix an issue with macOS.
- Fix tests to run on pushes to ``main`` and pull requests for ``main``.
- Configuration options spelled with hyphens in ``pyproject.toml``
  (e.g. ``line-length = 88``) are now supported.
- In debug log output mode, configuration options are now always spelled with hyphens
  instead of underscores.
- ``release_tools/update_contributors.py`` can now handle
  - GitHub usernames with RTL override characters
  - deleted GitHub users
- Black 24.2 compatibility by adding our own implementation of
  ``darkgraylib.files.find_project_root``.
- Updates to GitHub actions in CI builds:
  - ``actions/checkout`` from ``@v3`` to ``@v4``
  - ``actions/setup-python`` from ``@v4`` to ``@v5``
  - ``wearerequired/lint-action`` from ``@v2.1.0`` to ``@v2.3.0``
- Move test helpers used by both Darker and Graylint to importable modules.


Darker 0.1.0 to 1.7.0
=====================

For changes before the migration of code from Darker to Darkgraylib, see
`CHANGES.rst in the Darker repository`__.

__ https://github.com/akaihola/darker/blob/master/CHANGES.rst

.. _Unreleased: https://github.com/akaihola/darkgraylib/compare/v2.2.0...HEAD
.. _2.2.0: https://github.com/akaihola/darkgraylib/compare/v2.1.0...v2.2.0
.. _2.1.0: https://github.com/akaihola/darkgraylib/compare/v2.0.1...v2.1.0
.. _2.0.1: https://github.com/akaihola/darkgraylib/compare/v2.0.0...v2.0.1
.. _2.0.0: https://github.com/akaihola/darkgraylib/compare/v1.3.2...v2.0.0
.. _1.3.2: https://github.com/akaihola/darkgraylib/compare/v1.3.1...v1.3.2
.. _1.3.1: https://github.com/akaihola/darkgraylib/compare/v1.3.0...v1.3.1
.. _1.3.0: https://github.com/akaihola/darkgraylib/compare/v1.2.1...v1.3.0
.. _1.2.1: https://github.com/akaihola/darkgraylib/compare/v1.2.0...v1.2.1
.. _1.2.0: https://github.com/akaihola/darkgraylib/compare/v1.1.0...v1.2.0
.. _1.1.1: https://github.com/akaihola/darkgraylib/compare/v1.1.0...v1.1.1
.. _1.1.0: https://github.com/akaihola/darkgraylib/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/akaihola/darkgraylib/compare/1.7.0...v1.0.0

.. _uv: https://docs.astral.sh/uv/
.. _pyproject.toml: https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#writing-pyproject-toml
.. _Pytest: https://docs.pytest.org/
.. _setup.cfg: https://setuptools.pypa.io/en/latest/userguide/declarative_config.html
.. _resolution strategy: https://docs.astral.sh/uv/concepts/resolution/#resolution-strategy
.. _dependency groups: https://packaging.python.org/en/latest/specifications/dependency-groups/
.. _ANN101: https://docs.astral.sh/ruff/rules/missing-type-self/

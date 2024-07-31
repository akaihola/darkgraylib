Unreleased_
===========

These features will be included in the next release:

Added
-----

Fixed
-----


2.0.0_ - 2024-07-31
===================

Added
-----
- Return exit code 3 if command line parsing fails. We want to reserve 2 for file not
  found errors which will make GitHub actions easier. Also define constants for various
  exit codes to be used in Darkgraylib and applications which use it.


1.3.2_ - 2024-07-29
===================

Fixed
-----
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
- The command ``graylint --config=check-darkgraylib.toml`` now runs Flake8_, Mypy_,
  pydocstyle_, Pylint_ and Ruff_ on modified lines in Python files. Those tools are
  included in the ``[test]`` extra.
- Make the section name argument for the config dump function mandatory.

Removed
-------
- The config dump section name is now required and is not inferred from the caller.

Fixed
-----
- Update ``darkgray-dev-tools`` for Pip >= 24.1 compatibility.
- The `~darkgraylib.command_line.make_argument_parser` function now has a ``version``
  argument which defaults to Darkgraylib's own version. This allows Darker and Graylint
  to correctly report their own version when called with the ``--version`` option.


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

Removed
-------
- The ``release_tools/update_contributors.py`` script was moved to the
  ``darkgray-dev-tools`` repository.

Fixed
-----
- Badge links in the README on GitHub.
- Replace calls to the deprecated `datetime.datetime.utcfromtimestamp` method with
  `datetime.datetime.fromtimestamp`, passing it the timezone `datetime.timezone.utc`.


1.1.1_ - 2024-03-27
===================

Added
-----
- Support for Python 3.12 in the package metadata and the CI build.
- Run unit tests with the newest Black release, not a fixed version.
- In the future test, upgrade ``toml`` and ``Pygments`` to repository ``master``.
- Messages from future test are now generic, not Black-specific.
- Require ``click`` when running tests.

Removed
-------
- Dependency on Black, flynt, isort and regex.
- Obsolete Mypy configuration options.
- Skip tests on Python 3.13-dev in Windows and macOS. C extension builds are failing,
  this exclusion is to be removed when Python 3.13 has been removed.

Fixed
-----
- In the ``--update-readme`` command, escape pipe symbols (``|``) in the help output
  placed in the ``README.rst`` file.


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

.. _Unreleased: https://github.com/akaihola/darkgraylib/compare/v1.3.0...HEAD
.. _1.3.0: https://github.com/akaihola/darkgraylib/compare/v1.2.1...v1.3.0
.. _1.2.1: https://github.com/akaihola/darkgraylib/compare/v1.2.0...v1.2.1
.. _1.2.0: https://github.com/akaihola/darkgraylib/compare/v1.1.0...v1.2.0
.. _1.1.1: https://github.com/akaihola/darkgraylib/compare/v1.1.0...v1.1.1
.. _1.1.0: https://github.com/akaihola/darkgraylib/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/akaihola/darkgraylib/compare/1.7.0...v1.0.0

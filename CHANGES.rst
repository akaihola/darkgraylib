Unreleased_
===========

These features will be included in the next release:

Added
-----
- Support for Python 3.12 in the package metadata and the CI build.

Fixed
-----


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

.. _Unreleased: https://github.com/akaihola/darkgraylib/compare/v1.1.0...HEAD
.. _1.1.0: https://github.com/akaihola/darkgraylib/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/akaihola/darkgraylib/compare/1.7.0...v1.0.0

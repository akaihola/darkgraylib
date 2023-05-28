Unreleased_
===========

These features will be included in the next release:

Added
-----
- Copy the code base from Darker 1.7.0.
- Provide ``git_repo`` as a Pytest plugin.
- Configure the ``ruff`` linting tool.
- Drop support for Python 3.7.
- Allow ``-`` as the single source filename when using the ``--stdin-filename`` option.
  This makes the option compatible with Black.

Removed
-------
- Remove the Darker GitHub action.

Fixed
-----
- Use ``git worktree`` instead of ``git clone`` and ``git checkout`` to set up a
  temporary working tree for running linters for a baseline in the ``rev1`` revision of
  the repository.
- Include the ``py.typed`` typing marker in distributions.
- Fix tests path in Bandit configuration for CI.
- Python 3.12 compatibility in multi-line string scanning.
- Upgrade ``install-nix-action`` to version 22 in CI to fix an issue with macOS.
- Fix tests to run on pushes to ``main`` and pull requests for ``main``.


Darker 0.1.0 to 1.7.0
=====================

For changes before the migration of code from Darker to Darkgraylib, see
`CHANGES.rst in the Darker repository`__.

__ https://github.com/akaihola/darker/blob/master/CHANGES.rst

.. _Unreleased: https://github.com/akaihola/darker/compare/6515b5de...HEAD

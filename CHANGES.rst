Unreleased_
===========

These features will be included in the next release:

Added
-----
- Copy the code base from Darker 1.7.0.
- Provide ``git_repo`` as a Pytest plugin.
- Configure the ``ruff`` linting tool.

Fixed
-----
- Use ``git worktree`` instead of ``git clone`` and ``git checkout`` to set up a
  temporary working tree for running linters for a baseline in the ``rev1`` revision of
  the repository.
- Include the ``py.typed`` typing marker in distributions.
- Fix tests path in Bandit configuration for CI.


Darker 0.1.0 to 1.7.0
=====================

For changes before the migration of code from Darker to Darkgraylib, see
`CHANGES.rst in the Darker repository`__.

__ https://github.com/akaihola/darker/blob/master/CHANGES.rst

.. _Unreleased: https://github.com/akaihola/darker/compare/6515b5de...HEAD

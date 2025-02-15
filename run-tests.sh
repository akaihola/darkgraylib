#!/usr/bin/env bash

errors=0

VIRTUAL_ENV=
uv sync --quiet --all-groups --all-extras
UV_PYTHON=.venv

rm -f dist/*
uv build || errors=$?
uvx twine check dist/* || errors=$?
uv run pytest || errors=$?

exit $errors

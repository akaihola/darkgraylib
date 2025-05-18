#!/usr/bin/env bash

errors=0

uvx --with isort darker || errors=$?
uvx --with mypy --with pydocstyle --with pylint graylint || errors=$?

for file in "$@"; do
    case "$file" in
        *.yml|*.yaml)
            uvx yamllint "$file" || errors=$?
            ;;
        *.sh|*.md|*.rst|*.txt)
            uvx codespell "$file" || errors=$?
            ;;
    esac
done

exit $errors

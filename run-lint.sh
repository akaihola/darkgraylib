#!/usr/bin/env bash

VENV=$HOME/.virtualenvs/darker
PIP=${VENV}/bin/pip
[ ! -f ${PIP} ] && python -m venv ${VENV} && ${PIP} install -U pip
${PIP} install -q -e '.[color,test,release]'
${PIP} uninstall -q -y ruff

ensure() { command -v $1 >/dev/null || ${PIP} install -q $1; }

ensure black
ensure codespell

errors=0

source ${VENV}/bin/activate
for file in "$@"; do
    case "$file" in
        *.py)
            darker --quiet --isort --revision origin/main "$file" || errors=$?
            graylint --quiet --revision origin/main \
              --lint mypy \
              --lint "ruff check" \
              --lint "codespell" \
              "$file" || errors=$?
            ;;
        *.sh|*.md|*.rst|*.txt)
            codespell "$file" || errors=$?
            ;;
    esac
done
deactivate

exit $errors

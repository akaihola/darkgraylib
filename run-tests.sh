#!/usr/bin/env bash

VENV=$HOME/.virtualenvs/darker
PIP=${VENV}/bin/pip
[ ! -f ${PIP} ] && python -m venv ${VENV} && ${PIP} install -U pip
${PIP} install -q -e '.[color,test,release]'

errors=0
${VENV}/bin/pytest || errors=$?

exit $errors

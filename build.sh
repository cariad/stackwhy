#!/bin/env bash

set -euo pipefail

find . -name "*.sh" -not -path "*/.venv/*" -exec shellcheck -o all --severity style -x {} +

yamllint --strict .

if [ "${CI:=}" == "true" ]; then
  isort . --check-only --diff
else
  isort .
fi

if [ "${CI:=}" == "true" ]; then
  black . --check --diff
else
  black .
fi

flake8 .
mypy stackwhy
mypy tests

pytest -vv

if [[ -n ${1:-} ]]; then
  version=${1}
elif [[ -n ${CIRCLE_TAG:-} ]]; then
  version=${CIRCLE_TAG}
else
  version="-1.-1.-1"
fi

echo "${version}" > stackwhy/version/VERSION

pushd docsrc
rm -rf build
make
popd

rm -rf dist
python setup.py bdist_wheel
rm -rf build

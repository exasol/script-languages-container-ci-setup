#!/bin/bash
set -o errexit
set -o nounset
set -o pipefail


curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
export PATH=$PATH:$HOME/.poetry/bin
poetry --version

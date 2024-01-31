#!/usr/bin/env bash

set -x

# Find the location of where this script is stored, and set everything up in that directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

rm -rf "$SCRIPT_DIR"/src/parser/*.py
rm -rf "$SCRIPT_DIR"/src/parser/*.interp
rm -rf "$SCRIPT_DIR"/src/parser/*.tokens

chmod +x "$SCRIPT_DIR"/fix_formatting.sh

python3 -m venv "$SCRIPT_DIR"/env
source "$SCRIPT_DIR"/env/bin/activate

pip install antlr4-tools
pip install autopep8
antlr4 "$SCRIPT_DIR"/src/parser/* -Dlanguage=Python3

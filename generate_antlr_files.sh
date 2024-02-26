#!/usr/bin/env bash

# Find the location of where this script is stored, and set everything up in that directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

find "$SCRIPT_DIR"/src/parser -type f -not -name '*.g4' -not -name '__init__.py' -delete

antlr4 "$SCRIPT_DIR"/src/parser/*.g4 -Dlanguage=Python3 -visitor -no-listener -package parser

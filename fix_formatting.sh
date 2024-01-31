#!/usr/bin/env bash
#
# Find the location of where this script is stored, and set everything up in that directory
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

autopep8 --in-place --recursive $SCRIPT_DIR/src

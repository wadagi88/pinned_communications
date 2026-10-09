#!/bin/sh
# Regenerate every page. Run from anywhere.
cd "$(dirname "$0")" || exit 1
python3 build.py || exit 1
python3 lint.py

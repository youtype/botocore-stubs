#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

uv run pre-commit run --all-files
uv pip install -e . --config-settings editable_mode=compat
uv run istub -u

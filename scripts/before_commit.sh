#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

poetry run pyright
poetry run ruff check
poetry run ruff format --check
poetry run mypy botocore-stubs
poetry run istub -u

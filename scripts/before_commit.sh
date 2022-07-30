#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

poetry run flake8 botocore-stubs
poetry run black botocore-stubs
poetry run isort botocore-stubs
poetry run mypy botocore-stubs
poetry run istub -u

#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

npx pyright botocore-stubs
flake8 botocore-stubs
black botocore-stubs
isort botocore-stubs
mypy botocore-stubs
python -m istub -u

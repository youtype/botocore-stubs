#!/usr/bin/env bash
set -e

ROOT_PATH=$(dirname $(dirname $0))
cd $ROOT_PATH

uvx pre-commit run --all-files
uvx --with botocore --with . istub -u

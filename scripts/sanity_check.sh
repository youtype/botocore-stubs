#!/usr/bin/env bash
set -e

rm -rf dist/*
uv build --wheel
OUTPUT=`uvx --with dist/*.whl mypy test.py || true`
echo $OUTPUT
if [[ ${OUTPUT} != *"Found 1 error"* ]];then
    echo "Stubs test failed: $TEST"
    exit 1
fi

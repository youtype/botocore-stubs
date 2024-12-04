"""
Type annotations for botocore.translate module.

Copyright 2024 Vlad Emelianov
"""

from typing import Any

from botocore.utils import merge_dicts as merge_dicts

def build_retry_config(
    endpoint_prefix: str,
    retry_model: Any,
    definitions: Any,
    client_retry_config: Any | None = ...,
) -> Any: ...
def resolve_references(config: Any, definitions: Any) -> None: ...

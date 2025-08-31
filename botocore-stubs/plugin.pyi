"""
Type annotations for botocore.plugin module.

Copyright 2025 Vlad Emelianov
"""

import logging
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from botocore.client import BaseClient

log: logging.Logger = ...

@dataclass
class PluginContext:
    plugins: str | None = ...

def get_plugin_context() -> ContextVar[str | None]: ...
def set_plugin_context(ctx: Any) -> ContextVar[str | None]: ...
def reset_plugin_context(token: str | None) -> None: ...
def get_botocore_plugins() -> str | None: ...
def load_client_plugins(client: BaseClient, plugins: dict[str, str]) -> None: ...

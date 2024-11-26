"""
Copyright 2024 Vlad Emelianov
"""

from logging import Logger
from typing import Any, NamedTuple, TypeVar

from botocore.compat import accepts_kwargs as accepts_kwargs
from botocore.utils import EVENT_ALIASES as EVENT_ALIASES

logger: Logger = ...

_R = TypeVar("_R")

class _NodeList(NamedTuple):
    first: Any
    middle: Any
    last: Any

class NodeList(_NodeList):
    def __copy__(self: _R) -> _R: ...

def first_non_none_response(responses: Any, default: Any | None = ...) -> Any: ...

class BaseEventHooks:
    def emit(self, event_name: Any, **kwargs: Any) -> Any: ...
    def register(
        self,
        event_name: str,
        handler: Any,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    def register_first(
        self,
        event_name: str,
        handler: Any,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    def register_last(
        self,
        event_name: str,
        handler: Any,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    def unregister(
        self,
        event_name: str,
        handler: Any | None = ...,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...

class HierarchicalEmitter(BaseEventHooks):
    def __init__(self) -> None: ...
    def emit(self, event_name: str, **kwargs: Any) -> Any: ...
    def emit_until_response(self, event_name: str, **kwargs: Any) -> Any: ...
    def unregister(
        self,
        event_name: str,
        handler: Any | None = ...,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> None: ...
    def __copy__(self: _R) -> _R: ...

class EventAliaser(BaseEventHooks):
    def __init__(self, event_emitter: BaseEventHooks, event_aliases: Any | None = ...) -> None: ...
    def emit(self, event_name: str, **kwargs: Any) -> Any: ...
    def emit_until_response(self, event_name: str, **kwargs: Any) -> Any: ...
    def register(
        self,
        event_name: str,
        handler: Any,
        unique_id: Any | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> Any: ...
    def register_first(
        self,
        event_name: str,
        handler: Any,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> Any: ...
    def register_last(
        self,
        event_name: str,
        handler: Any,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> Any: ...
    def unregister(
        self,
        event_name: str,
        handler: Any | None = ...,
        unique_id: str | None = ...,
        unique_id_uses_count: bool = ...,
    ) -> Any: ...
    def __copy__(self: _R) -> _R: ...

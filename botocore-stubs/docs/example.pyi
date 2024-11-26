"""
Copyright 2024 Vlad Emelianov
"""

from typing import Any

from botocore.docs.shape import ShapeDocumenter
from botocore.model import Shape

class BaseExampleDocumenter(ShapeDocumenter):
    def document_example(
        self,
        section: Any,
        shape: Shape,
        prefix: str | None = ...,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
    ) -> None: ...
    def document_recursive_shape(self, section: Any, shape: Shape, **kwargs: Any) -> None: ...
    def document_shape_default(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_string(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_list(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_structure(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
        **kwargs: Any,
    ) -> None: ...
    def document_shape_type_map(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
        **kwargs: Any,
    ) -> None: ...

class ResponseExampleDocumenter(BaseExampleDocumenter):
    EVENT_NAME: str = ...
    def document_shape_type_event_stream(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        **kwargs: Any,
    ) -> None: ...

class RequestExampleDocumenter(BaseExampleDocumenter):
    EVENT_NAME: str = ...
    def document_shape_type_structure(
        self,
        section: Any,
        shape: Shape,
        history: Any,
        include: list[str] | None = ...,
        exclude: list[str] | None = ...,
        **kwargs: Any,
    ) -> None: ...

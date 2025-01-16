"""
Type annotations for botocore.parsers module.

Copyright 2025 Vlad Emelianov
"""

from logging import Logger
from typing import Any, Callable, Mapping

from botocore.compat import XMLParseError as XMLParseError
from botocore.eventstream import EventStream as EventStream
from botocore.eventstream import NoInitialResponseError as NoInitialResponseError
from botocore.model import Shape
from botocore.utils import is_json_value_header as is_json_value_header
from botocore.utils import lowercase_dict as lowercase_dict
from botocore.utils import merge_dicts as merge_dicts
from botocore.utils import parse_timestamp as parse_timestamp

LOG: Logger = ...
DEFAULT_TIMESTAMP_PARSER = parse_timestamp

class ResponseParserFactory:
    def __init__(self) -> None: ...
    def set_parser_defaults(self, **kwargs: Any) -> None: ...
    def create_parser(self, protocol_name: str) -> ResponseParser: ...

def create_parser(protocol: str) -> ResponseParser: ...

class ResponseParserError(Exception): ...

class ResponseParser:
    DEFAULT_ENCODING: str = ...
    EVENT_STREAM_PARSER_CLS: type[ResponseParser] | None = ...
    def __init__(
        self,
        timestamp_parser: Callable[[str], Any] | None = ...,
        blob_parser: Callable[[str], Any] | None = ...,
    ) -> None: ...
    def parse(self, response: Mapping[str, Any], shape: Shape) -> Any: ...

class BaseXMLResponseParser(ResponseParser):
    def __init__(
        self,
        timestamp_parser: Callable[[str], Any] | None = ...,
        blob_parser: Callable[[str], Any] | None = ...,
    ) -> None: ...

class QueryParser(BaseXMLResponseParser): ...
class EC2QueryParser(QueryParser): ...
class BaseJSONParser(ResponseParser): ...
class BaseEventStreamParser(ResponseParser): ...
class EventStreamJSONParser(BaseEventStreamParser, BaseJSONParser): ...
class EventStreamXMLParser(BaseEventStreamParser, BaseXMLResponseParser): ...
class JSONParser(BaseJSONParser): ...
class BaseRestParser(ResponseParser): ...
class RestJSONParser(BaseRestParser, BaseJSONParser): ...
class RestXMLParser(BaseRestParser, BaseXMLResponseParser): ...

PROTOCOL_PARSERS: dict[str, ResponseParser]

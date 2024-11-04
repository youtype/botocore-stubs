from collections.abc import MutableMapping
from logging import Logger
from typing import IO, Any, Dict, Iterator, Mapping, Optional, Type, TypeVar, Union

from botocore.compat import HTTPHeaders as HTTPHeaders
from botocore.compat import HTTPResponse as HTTPResponse
from botocore.compat import urlencode as urlencode
from botocore.compat import urlsplit as urlsplit
from botocore.compat import urlunsplit as urlunsplit
from botocore.exceptions import UnseekableStreamError as UnseekableStreamError
from urllib3.connection import HTTPConnection, VerifiedHTTPSConnection
from urllib3.connectionpool import HTTPConnectionPool, HTTPSConnectionPool

_R = TypeVar("_R")

logger: Logger = ...

class AWSHTTPResponse(HTTPResponse):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class AWSConnection:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.response_class: Any

    def close(self) -> None: ...
    def request(
        self,
        method: str,
        url: str,
        body: Any = ...,
        headers: Optional[Mapping[str, Any]] = ...,
        *args: Any,
        **kwargs: Any,
    ) -> HTTPConnection: ...
    def send(self, str: str) -> Any: ...

# FIXME: AWSConnection.send has incompatible arg names
class AWSHTTPConnection(AWSConnection, HTTPConnection): ...  # type: ignore [misc]
class AWSHTTPSConnection(AWSConnection, VerifiedHTTPSConnection): ...  # type: ignore [misc]

class AWSHTTPConnectionPool(HTTPConnectionPool):
    ConnectionCls: Type[AWSHTTPConnection]  # type: ignore [misc,assignment]

class AWSHTTPSConnectionPool(HTTPSConnectionPool):
    ConnectionCls: Type[AWSHTTPSConnection]  # type: ignore [misc,assignment]

def prepare_request_dict(
    request_dict: Mapping[str, Any],
    endpoint_url: str,
    context: Optional[Any] = ...,
    user_agent: Optional[str] = ...,
) -> None: ...
def create_request_object(request_dict: Mapping[str, Any]) -> Any: ...

class AWSPreparedRequest:
    def __init__(
        self,
        method: str,
        url: str,
        headers: HTTPHeaders,
        body: Union[str, bytes, bytearray, IO[bytes], IO[str], None],
        stream_output: bool,
    ) -> None:
        self.method: str
        self.url: str
        self.headers: HTTPHeaders
        self.body: Union[str, bytes, bytearray, IO[bytes], IO[str], None]
        self.stream_output: bool

    def reset_stream(self) -> None: ...

class AWSRequest:
    def __init__(
        self,
        method: Optional[str] = ...,
        url: Optional[str] = ...,
        headers: Optional[Mapping[str, Any]] = ...,
        data: Optional[Any] = ...,
        params: Optional[Mapping[str, Any]] = ...,
        auth_path: Optional[str] = ...,
        stream_output: bool = ...,
    ) -> None:
        self.method: Optional[str]
        self.url: Optional[str]
        self.headers: HTTPHeaders
        self.data: Optional[Any]
        self.params: Dict[str, Any]
        self.auth_path: Optional[str]
        self.stream_output: bool
        self.context: Dict[str, Any]

    def prepare(self) -> AWSPreparedRequest: ...
    @property
    def body(self) -> str: ...

class AWSRequestPreparer:
    def prepare(self, original: AWSRequest) -> AWSPreparedRequest: ...

class AWSResponse:
    def __init__(self, url: str, status_code: int, headers: HTTPHeaders, raw: Any) -> None:
        self.url: str
        self.status_code: int
        self.headers: HeadersDict
        self.raw: Any

    @property
    def content(self) -> bytes: ...
    @property
    def text(self) -> str: ...

class _HeaderKey:
    def __init__(self, key: str) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: Any) -> bool: ...

class HeadersDict(MutableMapping[str, str]):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __getitem__(self, key: str) -> Any: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def copy(self: _R) -> _R: ...

import datetime
import json
import logging
import os
import threading
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional

import dateutil.parser
from botocore import UNSIGNED
from botocore.compat import total_seconds
from botocore.config import Config
from botocore.credentials import JSONFileCache
from botocore.exceptions import ClientError, InvalidConfigError, TokenRetrievalError
from botocore.session import Session
from botocore.utils import CachedProperty, SSOTokenLoader
from dateutil.tz import tzutc

logger: logging.Logger

def create_token_resolver(session: Session) -> TokenProviderChain: ...
@dataclass(frozen=True)
class FrozenAuthToken:
    token: str
    expiration: Optional[datetime.datetime] = ...

class DeferredRefreshableToken:
    def __init__(
        self,
        method: Any,
        refresh_using: Callable[[], FrozenAuthToken],
        time_fetcher: Callable[[], datetime.datetime] = ...,
    ) -> None: ...
    def get_frozen_token(self) -> FrozenAuthToken: ...

class TokenProviderChain:
    def __init__(self, providers: Optional[Iterable[Any]] = ...) -> None: ...
    def load_token(self) -> DeferredRefreshableToken: ...

class SSOTokenProvider:
    METHOD: str = ...

    def __init__(
        self,
        session: Session,
        cache: Optional[JSONFileCache] = ...,
        time_fetcher: Callable[[], datetime.datetime] = ...,
    ) -> None: ...
    def load_token(self) -> DeferredRefreshableToken: ...

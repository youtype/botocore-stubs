"""
Type annotations for botocore.retries.standard module.

Copyright 2025 Vlad Emelianov
"""

from logging import Logger
from typing import Any, Callable, Sequence

from botocore.client import BaseClient
from botocore.exceptions import BotoCoreError
from botocore.exceptions import ConnectionError as ConnectionError
from botocore.exceptions import ConnectTimeoutError as ConnectTimeoutError
from botocore.exceptions import HTTPClientError as HTTPClientError
from botocore.exceptions import ReadTimeoutError as ReadTimeoutError
from botocore.model import OperationModel
from botocore.retries import quota as quota
from botocore.retries import special as special
from botocore.retries.base import BaseRetryableChecker as BaseRetryableChecker
from botocore.retries.base import BaseRetryBackoff as BaseRetryBackoff
from botocore.retries.quota import RetryQuota

logger: Logger = ...

DEFAULT_MAX_ATTEMPTS: int = ...

def register_retry_handler(client: BaseClient, max_attempts: int = ...) -> RetryHandler: ...

class RetryHandler:
    def __init__(
        self,
        retry_policy: RetryPolicy,
        retry_event_adapter: RetryEventAdapter,
        retry_quota: RetryQuota,
    ) -> None: ...
    def needs_retry(self, **kwargs: Any) -> float | None: ...

class RetryEventAdapter:
    def create_retry_context(self, **kwargs: Any) -> Any: ...
    def adapt_retry_response_from_context(self, context: RetryContext) -> None: ...

class RetryContext:
    def __init__(
        self,
        attempt_number: int,
        operation_model: OperationModel | None = ...,
        parsed_response: Any = ...,
        http_response: Any = ...,
        caught_exception: Exception | None = ...,
        request_context: Any = ...,
    ) -> None:
        self.attempt_number: int = ...
        self.operation_model: OperationModel | None = ...
        self.parsed_response: Any = ...
        self.http_response: Any = ...
        self.caught_exception: Exception | None = ...
        self.request_context: Any = ...

    def get_error_code(self) -> int | None: ...
    def add_retry_metadata(self, **kwargs: Any) -> None: ...
    def get_retry_metadata(self) -> Any: ...

class RetryPolicy:
    def __init__(
        self, retry_checker: BaseRetryableChecker, retry_backoff: BaseRetryBackoff
    ) -> None: ...
    def should_retry(self, context: RetryContext) -> Any: ...
    def compute_retry_delay(self, context: Any) -> float: ...

class ExponentialBackoff(BaseRetryBackoff):
    def __init__(self, max_backoff: int = ..., random: Callable[[], float] = ...) -> None: ...
    def delay_amount(self, context: RetryContext) -> float: ...

class MaxAttemptsChecker(BaseRetryableChecker):
    def __init__(self, max_attempts: int) -> None: ...
    def is_retryable(self, context: RetryContext) -> bool: ...

class TransientRetryableChecker(BaseRetryableChecker):
    def __init__(
        self,
        transient_error_codes: Sequence[str] | None = ...,
        transient_status_codes: Sequence[int] | None = ...,
        transient_exception_cls: Sequence[type[BotoCoreError]] | None = ...,
    ) -> None: ...
    def is_retryable(self, context: RetryContext) -> bool: ...

class ThrottledRetryableChecker(BaseRetryableChecker):
    def __init__(self, throttled_error_codes: Sequence[str] | None = ...) -> None: ...
    def is_retryable(self, context: RetryContext) -> bool: ...

class ModeledRetryableChecker(BaseRetryableChecker):
    def __init__(self) -> None: ...
    def is_retryable(self, context: RetryContext) -> Any: ...

class ModeledRetryErrorDetector:
    TRANSIENT_ERROR: str = ...
    THROTTLING_ERROR: str = ...
    def detect_error_type(self, context: RetryContext) -> Any: ...

class ThrottlingErrorDetector:
    def __init__(self, retry_event_adapter: Any) -> None: ...
    def is_throttling_error(self, **kwargs: Any) -> Any: ...

class StandardRetryConditions(BaseRetryableChecker):
    def __init__(self, max_attempts: Any = ...) -> None: ...
    def is_retryable(self, context: RetryContext) -> Any: ...

class OrRetryChecker(BaseRetryableChecker):
    def __init__(self, checkers: Any) -> None: ...
    def is_retryable(self, context: RetryContext) -> Any: ...

class RetryQuotaChecker:
    def __init__(self, quota: Any) -> None: ...  # noqa: F811
    def acquire_retry_quota(self, context: RetryContext) -> bool: ...
    def release_retry_quota(
        self, context: RetryContext, http_response: Any, **kwargs: Any
    ) -> None: ...

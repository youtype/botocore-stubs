"""
Copyright 2024 Vlad Emelianov
"""

from logging import Logger
from typing import Any

from botocore.retries.base import BaseRetryableChecker as BaseRetryableChecker

logger: Logger = ...

class RetryIDPCommunicationError(BaseRetryableChecker):
    def is_retryable(self, context: Any) -> Any: ...

class RetryDDBChecksumError(BaseRetryableChecker):
    def is_retryable(self, context: Any) -> Any: ...

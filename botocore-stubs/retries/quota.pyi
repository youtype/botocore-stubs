"""
Type annotations for botocore.retries.quota module.

Copyright 2024 Vlad Emelianov
"""

from typing import Any

class RetryQuota:
    INITIAL_CAPACITY: int = ...
    def __init__(self, initial_capacity: Any = ..., lock: Any | None = ...) -> None: ...
    def acquire(self, capacity_amount: Any) -> Any: ...
    def release(self, capacity_amount: Any) -> None: ...
    @property
    def available_capacity(self) -> Any: ...

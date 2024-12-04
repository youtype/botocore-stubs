"""
Type annotations for botocore.regions module.

Copyright 2024 Vlad Emelianov
"""

from enum import Enum
from logging import Logger
from typing import Any, Mapping

from botocore.auth import AUTH_TYPE_MAPS as AUTH_TYPE_MAPS
from botocore.compat import HAS_CRT as HAS_CRT
from botocore.crt import CRT_SUPPORTED_AUTH_TYPES as CRT_SUPPORTED_AUTH_TYPES
from botocore.endpoint_provider import RuleSetEndpoint
from botocore.exceptions import BotoCoreError
from botocore.exceptions import NoRegionError as NoRegionError
from botocore.hooks import BaseEventHooks
from botocore.model import OperationModel, ServiceModel

LOG: Logger = ...
DEFAULT_URI_TEMPLATE: str
DEFAULT_SERVICE_DATA: dict[str, dict[str, Any]]

class BaseEndpointResolver:
    def construct_endpoint(self, service_name: str, region_name: str | None = ...) -> None: ...
    def get_available_partitions(self) -> list[str]: ...
    def get_available_endpoints(
        self,
        service_name: str,
        partition_name: str = ...,
        allow_non_regional: bool = ...,
    ) -> list[str]: ...

class EndpointResolver(BaseEndpointResolver):
    def __init__(self, endpoint_data: Mapping[str, Any], uses_builtin_data: bool = ...) -> None: ...
    def get_service_endpoints_data(self, service_name: str, partition_name: str = ...) -> Any: ...
    def get_available_partitions(self) -> list[str]: ...
    def get_available_endpoints(
        self,
        service_name: str,
        partition_name: str = ...,
        allow_non_regional: bool = ...,
        endpoint_variant_tags: Any = ...,
    ) -> list[str]: ...
    def get_partition_dns_suffix(
        self, partition_name: str, endpoint_variant_tags: Any = ...
    ) -> str: ...
    def construct_endpoint(  # type: ignore [override]
        self,
        service_name: str,
        region_name: str | None = ...,
        partition_name: str | None = ...,
        use_dualstack_endpoint: bool = ...,
        use_fips_endpoint: bool = ...,
    ) -> dict[str, Any] | None: ...
    def get_partition_for_region(self, region_name: str) -> str: ...

class EndpointResolverBuiltins(Enum):
    AWS_REGION: str
    AWS_USE_FIPS: str
    AWS_USE_DUALSTACK: str
    AWS_STS_USE_GLOBAL_ENDPOINT: str
    AWS_S3_USE_GLOBAL_ENDPOINT: str
    AWS_S3_ACCELERATE: str
    AWS_S3_FORCE_PATH_STYLE: str
    AWS_S3_USE_ARN_REGION: str
    AWS_S3CONTROL_USE_ARN_REGION: str
    AWS_S3_DISABLE_MRAP: str
    SDK_ENDPOINT: str
    ACCOUNT_ID: str
    ACCOUNT_ID_ENDPOINT_MODE: str

class EndpointRulesetResolver:
    def __init__(
        self,
        endpoint_ruleset_data: Mapping[str, Any],
        partition_data: Mapping[str, Any],
        service_model: ServiceModel,
        builtins: EndpointResolverBuiltins,
        client_context: Any,
        event_emitter: BaseEventHooks,
        use_ssl: bool = ...,
        requested_auth_scheme: str | None = ...,
    ) -> None: ...
    def construct_endpoint(
        self,
        operation_model: OperationModel,
        call_args: Mapping[str, Any] | None,
        request_context: Any,
    ) -> RuleSetEndpoint: ...
    def auth_schemes_to_signing_ctx(
        self, auth_schemes: list[Mapping[str, Any]]
    ) -> tuple[str, dict[str, Any]]: ...
    def ruleset_error_to_botocore_exception(
        self, ruleset_exception: Exception, params: Mapping[str, Any]
    ) -> BotoCoreError: ...

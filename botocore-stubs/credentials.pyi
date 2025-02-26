"""
Type annotations for botocore.credentials module.

Copyright 2025 Vlad Emelianov
"""

import datetime
from logging import Logger
from typing import Any, Callable, Mapping, NamedTuple, TypeVar

from botocore.client import BaseClient
from botocore.compat import compat_shell_split as compat_shell_split
from botocore.compat import total_seconds as total_seconds
from botocore.config import Config as Config
from botocore.exceptions import ConfigNotFound as ConfigNotFound
from botocore.exceptions import CredentialRetrievalError as CredentialRetrievalError
from botocore.exceptions import InfiniteLoopConfigError as InfiniteLoopConfigError
from botocore.exceptions import InvalidConfigError as InvalidConfigError
from botocore.exceptions import MetadataRetrievalError as MetadataRetrievalError
from botocore.exceptions import PartialCredentialsError as PartialCredentialsError
from botocore.exceptions import RefreshWithMFAUnsupportedError as RefreshWithMFAUnsupportedError
from botocore.exceptions import UnauthorizedSSOTokenError as UnauthorizedSSOTokenError
from botocore.exceptions import UnknownCredentialError as UnknownCredentialError
from botocore.session import Session
from botocore.tokens import SSOTokenProvider
from botocore.utils import ContainerMetadataFetcher as ContainerMetadataFetcher
from botocore.utils import FileWebIdentityTokenLoader as FileWebIdentityTokenLoader
from botocore.utils import InstanceMetadataFetcher as InstanceMetadataFetcher
from botocore.utils import SSOTokenLoader as SSOTokenLoader
from botocore.utils import parse_key_val_file as parse_key_val_file

_R = TypeVar("_R")

logger: Logger = ...

class ReadOnlyCredentials(NamedTuple):
    access_key: str | None
    secret_key: str | None
    token: str | None
    account_id: str | None = ...

def create_credential_resolver(
    session: Session,
    cache: dict[str, Any] | None = ...,
    region_name: str | None = ...,
) -> CredentialResolver: ...

class ProfileProviderBuilder:
    def __init__(
        self,
        session: Session,
        cache: dict[str, Any] | None = ...,
        region_name: str | None = ...,
        sso_token_cache: dict[str, Any] | None = ...,
    ) -> None: ...
    def providers(
        self, profile_name: str, disable_env_vars: bool = ...
    ) -> list[CredentialProvider]: ...

def get_credentials(session: Session) -> Credentials: ...
def create_assume_role_refresher(client: BaseClient, params: Any) -> Any: ...
def create_mfa_serial_refresher(actual_refresh: Any) -> Any: ...

class Credentials:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        token: str | None = ...,
        method: str | None = ...,
        account_id: str | None = ...,
    ) -> None:
        self.access_key: str = ...
        self.secret_key: str = ...
        self.token: str | None = ...
        self.method: str = ...

    def get_frozen_credentials(self) -> ReadOnlyCredentials: ...
    def get_deferred_property(self, property_name: str) -> Callable[[], str | None]: ...

class RefreshableCredentials(Credentials):
    method: Any = ...
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        token: str,
        expiry_time: datetime.datetime,
        refresh_using: Callable[[], Any],
        method: str,
        time_fetcher: Callable[[], datetime.datetime] | None = ...,
        advisory_timeout: int | None = ...,
        mandatory_timeout: int | None = ...,
        account_id: str | None = ...,
    ) -> None: ...
    @classmethod
    def create_from_metadata(
        cls: type[_R],
        metadata: dict[str, Any],
        refresh_using: Callable[[], Any],
        method: Any,
        advisory_timeout: int | None = ...,
        mandatory_timeout: int | None = ...,
    ) -> _R: ...
    @property  # type: ignore [override]
    def access_key(self) -> str: ...  # type: ignore [override]
    @access_key.setter
    def access_key(self, value: str) -> None: ...
    @property  # type: ignore [override]
    def secret_key(self) -> str: ...  # type: ignore [override]
    @secret_key.setter
    def secret_key(self, value: str) -> None: ...
    @property  # type: ignore [override]
    def token(self) -> str: ...  # type: ignore [override]
    @token.setter
    def token(self, value: str) -> None: ...
    @property
    def account_id(self) -> str: ...
    @account_id.setter
    def account_id(self, value: str) -> None: ...
    def refresh_needed(self, refresh_in: int | None = ...) -> bool: ...
    def get_frozen_credentials(self) -> ReadOnlyCredentials: ...

class DeferredRefreshableCredentials(RefreshableCredentials):
    def __init__(
        self,
        refresh_using: Callable[[], Any],
        method: Any,
        time_fetcher: Callable[[], datetime.datetime] | None = ...,
    ) -> None:
        self.method: Any = ...

    def refresh_needed(self, refresh_in: int | None = ...) -> bool: ...

class CachedCredentialFetcher:
    DEFAULT_EXPIRY_WINDOW_SECONDS: int = ...
    def __init__(
        self, cache: Any | None = ..., expiry_window_seconds: int | None = ...
    ) -> None: ...
    def fetch_credentials(self) -> dict[str, Any]: ...

class BaseAssumeRoleCredentialFetcher(CachedCredentialFetcher):
    def __init__(
        self,
        client_creator: Callable[[], BaseClient],
        role_arn: str,
        extra_args: Any | None = ...,
        cache: Any | None = ...,
        expiry_window_seconds: Any | None = ...,
    ) -> None: ...

class AssumeRoleCredentialFetcher(BaseAssumeRoleCredentialFetcher):
    def __init__(
        self,
        client_creator: Callable[[], BaseClient],
        source_credentials: Any,
        role_arn: str,
        extra_args: dict[str, Any] | None = ...,
        mfa_prompter: Callable[..., Any] | None = ...,
        cache: dict[str, Any] | None = ...,
        expiry_window_seconds: int | None = ...,
    ) -> None: ...

class AssumeRoleWithWebIdentityCredentialFetcher(BaseAssumeRoleCredentialFetcher):
    def __init__(
        self,
        client_creator: Callable[[], BaseClient],
        web_identity_token_loader: Callable[[], str],
        role_arn: str,
        extra_args: Any | None = ...,
        cache: dict[str, Any] | None = ...,
        expiry_window_seconds: int | None = ...,
    ) -> None: ...

class CredentialProvider:
    METHOD: str | None = ...
    CANONICAL_NAME: str | None = ...
    def __init__(self, session: Session | None = ...) -> None:
        self.session: Session = ...

    def load(self) -> Any: ...

class ProcessProvider(CredentialProvider):
    METHOD: str = ...
    def __init__(
        self, profile_name: str, load_config: Callable[..., Any], popen: Callable[..., Any] = ...
    ) -> None: ...
    def load(self) -> Credentials | None: ...
    @property
    def profile_config(self) -> dict[str, Any]: ...

class InstanceMetadataProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    def __init__(self, iam_role_fetcher: InstanceMetadataFetcher) -> None: ...
    def load(self) -> Credentials | None: ...

class EnvProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    TOKENS: list[str] = ...
    EXPIRY_TIME: str = ...
    ACCOUNT_ID: str = ...
    def __init__(
        self, environ: Mapping[str, Any] | None = ..., mapping: Mapping[str, Any] | None = ...
    ) -> None:
        self.environ: Mapping[str, Any] = ...

    def load(self) -> Credentials | None: ...

class OriginalEC2Provider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    CRED_FILE_ENV: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    def __init__(
        self, environ: Mapping[str, str] | None = ..., parser: Callable[..., Any] | None = ...
    ) -> None: ...
    def load(self) -> Credentials | None: ...

class SharedCredentialProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    TOKENS: list[str] = ...
    ACCOUNT_ID: str = ...
    def __init__(
        self,
        creds_filename: str,
        profile_name: str | None = ...,
        ini_parser: Any | None = ...,
    ) -> None: ...
    def load(self) -> Credentials | None: ...

class ConfigProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    TOKENS: list[str] = ...
    ACCOUNT_ID: str = ...
    def __init__(
        self,
        config_filename: str,
        profile_name: str,
        config_parser: Any | None = ...,
    ) -> None: ...
    def load(self) -> Credentials | None: ...

class BotoProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    BOTO_CONFIG_ENV: str = ...
    DEFAULT_CONFIG_FILENAMES: list[str] = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    def __init__(self, environ: Any | None = ..., ini_parser: Any | None = ...) -> None: ...
    def load(self) -> Credentials | None: ...

class AssumeRoleProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: None = ...
    ROLE_CONFIG_VAR: str = ...
    WEB_IDENTITY_TOKE_FILE_VAR: str = ...
    EXPIRY_WINDOW_SECONDS: int = ...
    def __init__(
        self,
        load_config: Callable[[], Mapping[str, Any]],
        client_creator: Callable[..., Any],
        cache: dict[str, Any],
        profile_name: str,
        prompter: Callable[..., Any] = ...,
        credential_sourcer: CanonicalNameCredentialSourcer | None = ...,
        profile_provider_builder: Any | None = ...,
    ) -> None:
        self.cache: dict[str, Any] = ...
    def load(self) -> DeferredRefreshableCredentials | None: ...

class AssumeRoleWithWebIdentityProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: None = ...
    def __init__(
        self,
        load_config: Callable[[], Mapping[str, Any]],
        client_creator: Callable[..., Any],
        profile_name: str,
        cache: dict[str, Any] | None = ...,
        disable_env_vars: bool = ...,
        token_loader_cls: type[FileWebIdentityTokenLoader] | None = ...,
    ) -> None:
        self.cache: dict[str, Any] = ...
    def load(self) -> DeferredRefreshableCredentials | None: ...

class CanonicalNameCredentialSourcer:
    def __init__(self, providers: list[CredentialProvider]) -> None: ...
    def is_supported(self, source_name: str) -> bool: ...
    def source_credentials(self, source_name: str) -> Credentials: ...

class ContainerProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ENV_VAR: str = ...
    ENV_VAR_FULL: str = ...
    ENV_VAR_AUTH_TOKEN: str = ...
    ENV_VAR_AUTH_TOKEN_FILE: str = ...
    def __init__(
        self,
        environ: Mapping[str, str] | None = ...,
        fetcher: AssumeRoleCredentialFetcher | None = ...,
    ) -> None: ...
    def load(self) -> RefreshableCredentials: ...

class CredentialResolver:
    providers: list[CredentialProvider]
    def __init__(self, providers: list[CredentialProvider]) -> None: ...
    def insert_before(self, name: str, credential_provider: CredentialProvider) -> None: ...
    def insert_after(self, name: str, credential_provider: CredentialProvider) -> None: ...
    def remove(self, name: str) -> None: ...
    def get_provider(self, name: str) -> CredentialProvider: ...
    def load_credentials(self) -> Credentials | None: ...

class SSOCredentialFetcher(CachedCredentialFetcher):
    def __init__(
        self,
        start_url: str,
        sso_region: str,
        role_name: str,
        account_id: str,
        client_creator: Callable[..., Any],
        token_loader: Callable[[], str] | None = ...,
        cache: dict[str, Any] | None = ...,
        expiry_window_seconds: float | None = ...,
        token_provider: SSOTokenProvider | None = ...,
        sso_session_name: str | None = ...,
    ) -> None: ...

class SSOProvider(CredentialProvider):
    METHOD: str = ...
    def __init__(
        self,
        load_config: Callable[[], Any],
        client_creator: Callable[..., Any],
        profile_name: str,
        cache: dict[str, Any] | None = ...,
        token_cache: dict[str, Any] | None = ...,
        token_provider: SSOTokenProvider | None = ...,
    ) -> None:
        self.cache: dict[str, Any] = ...
    def load(self) -> DeferredRefreshableCredentials: ...

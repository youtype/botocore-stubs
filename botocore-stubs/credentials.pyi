from logging import Logger
from typing import Any, Callable, Dict, List, Mapping, NamedTuple, Optional

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

logger: Logger = ...

class ReadOnlyCredentials(NamedTuple):
    access_key: str
    secret_key: str
    token: str

def create_credential_resolver(
    session: Session,
    cache: Optional[Dict[str, Any]] = ...,
    region_name: Optional[str] = ...,
) -> CredentialResolver: ...

class ProfileProviderBuilder:
    def __init__(
        self,
        session: Session,
        cache: Optional[Dict[str, Any]] = ...,
        region_name: Optional[str] = ...,
        sso_token_cache: Optional[Dict[str, Any]] = ...,
    ) -> None: ...
    def providers(
        self, profile_name: str, disable_env_vars: bool = ...
    ) -> List[CredentialProvider]: ...

def get_credentials(session: Session) -> Any: ...
def create_assume_role_refresher(client: Any, params: Any) -> Any: ...
def create_mfa_serial_refresher(actual_refresh: Any) -> Any: ...

class Credentials:
    access_key: str = ...
    secret_key: str = ...
    token: str = ...
    method: str = ...
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        token: Optional[str] = ...,
        method: Optional[str] = ...,
    ) -> None: ...
    def get_frozen_credentials(self) -> ReadOnlyCredentials: ...

class RefreshableCredentials(Credentials):
    method: Any = ...
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        token: str,
        expiry_time: Any,
        refresh_using: Any,
        method: str,
        time_fetcher: Any = ...,
        advisory_timeout: Optional[int] = ...,
        mandatory_timeout: Optional[int] = ...,
    ) -> None: ...
    @classmethod
    def create_from_metadata(
        cls,
        metadata: Any,
        refresh_using: Any,
        method: Any,
        advisory_timeout: Optional[int] = ...,
        mandatory_timeout: Optional[int] = ...,
    ) -> Any: ...
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
    def refresh_needed(self, refresh_in: Optional[Any] = ...) -> Any: ...
    def get_frozen_credentials(self) -> ReadOnlyCredentials: ...

class DeferredRefreshableCredentials(RefreshableCredentials):
    method: Any = ...
    def __init__(self, refresh_using: Any, method: Any, time_fetcher: Any = ...) -> None: ...
    def refresh_needed(self, refresh_in: Optional[Any] = ...) -> Any: ...

class CachedCredentialFetcher:
    DEFAULT_EXPIRY_WINDOW_SECONDS: Any = ...
    def __init__(
        self, cache: Optional[Any] = ..., expiry_window_seconds: Optional[Any] = ...
    ) -> None: ...
    def fetch_credentials(self) -> Any: ...

class BaseAssumeRoleCredentialFetcher(CachedCredentialFetcher):
    def __init__(
        self,
        client_creator: Any,
        role_arn: str,
        extra_args: Optional[Any] = ...,
        cache: Optional[Any] = ...,
        expiry_window_seconds: Optional[Any] = ...,
    ) -> None: ...

class AssumeRoleCredentialFetcher(BaseAssumeRoleCredentialFetcher):
    def __init__(
        self,
        client_creator: Any,
        source_credentials: Any,
        role_arn: str,
        extra_args: Optional[Any] = ...,
        mfa_prompter: Optional[Any] = ...,
        cache: Optional[Any] = ...,
        expiry_window_seconds: Optional[Any] = ...,
    ) -> None: ...

class AssumeRoleWithWebIdentityCredentialFetcher(BaseAssumeRoleCredentialFetcher):
    def __init__(
        self,
        client_creator: Any,
        web_identity_token_loader: Any,
        role_arn: str,
        extra_args: Optional[Any] = ...,
        cache: Optional[Any] = ...,
        expiry_window_seconds: Optional[Any] = ...,
    ) -> None: ...

class CredentialProvider:
    METHOD: Optional[str] = ...
    CANONICAL_NAME: Optional[str] = ...
    def __init__(self, session: Optional[Session] = ...) -> None:
        self.session: Session = ...

    def load(self) -> Any: ...

class ProcessProvider(CredentialProvider):
    METHOD: str = ...
    def __init__(self, profile_name: str, load_config: Any, popen: Any = ...) -> None: ...
    def load(self) -> Any: ...

class InstanceMetadataProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    def __init__(self, iam_role_fetcher: Any) -> None: ...
    def load(self) -> Any: ...

class EnvProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    TOKENS: Any = ...
    EXPIRY_TIME: str = ...
    environ: Any = ...
    def __init__(self, environ: Optional[Any] = ..., mapping: Optional[Any] = ...) -> None: ...
    def load(self) -> Any: ...

class OriginalEC2Provider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    CRED_FILE_ENV: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    def __init__(self, environ: Optional[Any] = ..., parser: Optional[Any] = ...) -> None: ...
    def load(self) -> Any: ...

class SharedCredentialProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    TOKENS: Any = ...
    def __init__(
        self,
        creds_filename: Any,
        profile_name: Optional[Any] = ...,
        ini_parser: Optional[Any] = ...,
    ) -> None: ...
    def load(self) -> Any: ...

class ConfigProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    TOKENS: Any = ...
    def __init__(
        self,
        config_filename: Any,
        profile_name: str,
        config_parser: Optional[Any] = ...,
    ) -> None: ...
    def load(self) -> Any: ...

class BotoProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: str = ...
    BOTO_CONFIG_ENV: str = ...
    DEFAULT_CONFIG_FILENAMES: Any = ...
    ACCESS_KEY: str = ...
    SECRET_KEY: str = ...
    def __init__(self, environ: Optional[Any] = ..., ini_parser: Optional[Any] = ...) -> None: ...
    def load(self) -> Optional[Credentials]: ...

class AssumeRoleProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: Any = ...
    ROLE_CONFIG_VAR: str = ...
    WEB_IDENTITY_TOKE_FILE_VAR: str = ...
    EXPIRY_WINDOW_SECONDS: Any = ...
    cache: Any = ...
    def __init__(
        self,
        load_config: Callable[[], Mapping[str, Any]],
        client_creator: Callable[..., Any],
        cache: Dict[str, Any],
        profile_name: str,
        prompter: Callable[..., Any] = ...,
        credential_sourcer: Optional[CanonicalNameCredentialSourcer] = ...,
        profile_provider_builder: Optional[Any] = ...,
    ) -> None: ...
    def load(self) -> DeferredRefreshableCredentials: ...

class AssumeRoleWithWebIdentityProvider(CredentialProvider):
    METHOD: str = ...
    CANONICAL_NAME: Any = ...
    cache: Any = ...
    def __init__(
        self,
        load_config: Any,
        client_creator: Any,
        profile_name: str,
        cache: Optional[Any] = ...,
        disable_env_vars: bool = ...,
        token_loader_cls: Optional[Any] = ...,
    ) -> None: ...
    def load(self) -> Optional[DeferredRefreshableCredentials]: ...

class CanonicalNameCredentialSourcer:
    def __init__(self, providers: List[CredentialProvider]) -> None: ...
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
        self, environ: Optional[Mapping[str, str]] = ..., fetcher: Optional[Any] = ...
    ) -> None: ...
    def load(self) -> RefreshableCredentials: ...

class CredentialResolver:
    providers: List[CredentialProvider]
    def __init__(self, providers: List[CredentialProvider]) -> None: ...
    def insert_before(self, name: str, credential_provider: CredentialProvider) -> None: ...
    def insert_after(self, name: str, credential_provider: CredentialProvider) -> None: ...
    def remove(self, name: str) -> None: ...
    def get_provider(self, name: str) -> CredentialProvider: ...
    def load_credentials(self) -> Optional[Credentials]: ...

class SSOCredentialFetcher(CachedCredentialFetcher):
    def __init__(
        self,
        start_url: Any,
        sso_region: Any,
        role_name: Any,
        account_id: Any,
        client_creator: Any,
        token_loader: Optional[Any] = ...,
        cache: Optional[Any] = ...,
        expiry_window_seconds: Optional[Any] = ...,
        token_provider: Optional[SSOTokenProvider] = ...,
        sso_session_name: Optional[str] = ...,
    ) -> None: ...

class SSOProvider(CredentialProvider):
    METHOD: str = ...
    cache: Any = ...
    def __init__(
        self,
        load_config: Any,
        client_creator: Any,
        profile_name: str,
        cache: Optional[Any] = ...,
        token_cache: Optional[Any] = ...,
        token_provider: Optional[SSOTokenProvider] = ...,
    ) -> None: ...
    def load(self) -> DeferredRefreshableCredentials: ...

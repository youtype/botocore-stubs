from typing import Any, Mapping, Optional, Union

from botocore.awsrequest import create_request_object as create_request_object
from botocore.awsrequest import prepare_request_dict as prepare_request_dict
from botocore.compat import OrderedDict as OrderedDict
from botocore.credentials import Credentials, ReadOnlyCredentials
from botocore.exceptions import UnknownClientMethodError as UnknownClientMethodError
from botocore.exceptions import UnknownSignatureVersionError as UnknownSignatureVersionError
from botocore.exceptions import UnsupportedSignatureVersionError as UnsupportedSignatureVersionError
from botocore.hooks import BaseEventHooks
from botocore.model import ServiceId
from botocore.utils import datetime2timestamp as datetime2timestamp

_CredentialsUnion = Union[Credentials, ReadOnlyCredentials]

class RequestSigner:
    def __init__(
        self,
        service_id: ServiceId,
        region_name: str,
        signing_name: str,
        signature_version: str,
        credentials: _CredentialsUnion,
        event_emitter: BaseEventHooks,
        auth_token: Optional[str] = ...,
    ) -> None: ...
    @property
    def region_name(self) -> str: ...
    @property
    def signature_version(self) -> str: ...
    @property
    def signing_name(self) -> str: ...
    def handler(
        self, operation_name: Optional[str] = ..., request: Optional[Any] = ..., **kwargs: Any
    ) -> Any: ...
    def sign(
        self,
        operation_name: str,
        request: Any,
        region_name: Optional[str] = ...,
        signing_type: str = ...,
        expires_in: Optional[Any] = ...,
        signing_name: Optional[str] = ...,
    ) -> None: ...
    def get_auth_instance(
        self,
        signing_name: str,
        region_name: str,
        signature_version: Optional[str] = ...,
        request_credentials: Optional[_CredentialsUnion] = ...,
        **kwargs: Any,
    ) -> Any: ...
    get_auth: Any = ...
    def generate_presigned_url(
        self,
        request_dict: Mapping[str, Any],
        operation_name: str,
        expires_in: int = ...,
        region_name: Optional[str] = ...,
        signing_name: Optional[str] = ...,
    ) -> Any: ...

class CloudFrontSigner:
    key_id: Any = ...
    rsa_signer: Any = ...
    def __init__(self, key_id: str, rsa_signer: Any) -> None: ...
    def generate_presigned_url(
        self, url: str, date_less_than: Optional[Any] = ..., policy: Optional[Any] = ...
    ) -> str: ...
    def build_policy(
        self,
        resource: Any,
        date_less_than: Any,
        date_greater_than: Optional[Any] = ...,
        ip_address: Optional[Any] = ...,
    ) -> str: ...

def add_generate_db_auth_token(class_attributes: Any, **kwargs: Any) -> None: ...
def generate_db_auth_token(
    self: Any, DBHostname: Any, Port: Any, DBUsername: Any, Region: Optional[Any] = ...
) -> Any: ...

class S3PostPresigner:
    def __init__(self, request_signer: Any) -> None: ...
    def generate_presigned_post(
        self,
        request_dict: Mapping[str, Any],
        fields: Optional[Any] = ...,
        conditions: Optional[Any] = ...,
        expires_in: int = ...,
        region_name: Optional[str] = ...,
    ) -> Any: ...

def add_generate_presigned_url(class_attributes: Any, **kwargs: Any) -> None: ...
def generate_presigned_url(
    self: Any,
    ClientMethod: Any,
    Params: Optional[Any] = ...,
    ExpiresIn: int = ...,
    HttpMethod: Optional[Any] = ...,
) -> Any: ...
def add_generate_presigned_post(class_attributes: Any, **kwargs: Any) -> None: ...
def generate_presigned_post(
    self: Any,
    Bucket: Any,
    Key: Any,
    Fields: Optional[Any] = ...,
    Conditions: Optional[Any] = ...,
    ExpiresIn: int = ...,
) -> Any: ...

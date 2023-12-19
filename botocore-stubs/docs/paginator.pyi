from typing import Any

class PaginatorDocumenter:
    def __init__(self, client: Any, service_paginator_model: Any, root_docs_path: Any) -> None: ...
    def document_paginators(self, section: Any) -> None: ...

def document_paginate_method(
    section: Any,
    paginator_name: str,
    event_emitter: Any,
    service_model: Any,
    paginator_config: Any,
    include_signature: bool = ...,
) -> None: ...

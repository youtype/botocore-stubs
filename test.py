from botocore.compat import ensure_bytes

ensure_bytes("foo")
ensure_bytes(b"foo")
ensure_bytes(None)

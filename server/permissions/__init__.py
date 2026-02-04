"""Scoped permissions and API key authentication stub."""

from __future__ import annotations

import os
from typing import Sequence

from flask import g, request

from server.errors import UnauthorizedError

# Scope names aligned with tool categories
SCOPE_READ = "read"
SCOPE_WRITE = "write"
SCOPE_DESTRUCTIVE = "destructive"

# Header / env for API key (stub: single key from env)
API_KEY_HEADER = "X-API-Key"
AUTH_HEADER = "Authorization"
ENV_API_KEY = "MCP_API_KEY"


def get_api_key_from_request() -> str | None:
    """Extract API key from X-API-Key or Authorization: Bearer <key>."""
    key = request.headers.get(API_KEY_HEADER)
    if key:
        return key
    auth = request.headers.get(AUTH_HEADER)
    if auth and auth.startswith("Bearer "):
        return auth[7:].strip()
    return None


def get_expected_api_key() -> str | None:
    """Expected API key from environment (stub: single shared key)."""
    return os.environ.get(ENV_API_KEY)


def authenticate_request() -> None:
    """
    Validate API key and set g.scopes for the request.
    Raises UnauthorizedError if invalid or missing.
    Stub: valid key gets all scopes [read, write, destructive].
    """
    key = get_api_key_from_request()
    expected = get_expected_api_key()

    # Optional auth: if no key is configured, allow all (dev mode)
    if not expected:
        g.scopes = [SCOPE_READ, SCOPE_WRITE, SCOPE_DESTRUCTIVE]
        g.authenticated = True
        return

    if not key or key != expected:
        raise UnauthorizedError()

    g.scopes = [SCOPE_READ, SCOPE_WRITE, SCOPE_DESTRUCTIVE]
    g.authenticated = True


def has_scope(required_scope: str) -> bool:
    """Check if the current request has the given permission scope."""
    scopes: Sequence[str] = getattr(g, "scopes", [])
    return required_scope in scopes


def require_scope(required_scope: str) -> None:
    """Raise PermissionDeniedError if request does not have the scope."""
    from server.errors import PermissionDeniedError

    if not has_scope(required_scope):
        raise PermissionDeniedError(
            f"Permission denied: scope '{required_scope}' required"
        )

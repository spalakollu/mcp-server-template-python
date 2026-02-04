"""Standardized error types and JSON-RPC error responses."""

from __future__ import annotations

from typing import Any


# JSON-RPC 2.0 standard codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603

# Application-specific (use -32xxx range or 4xx)
UNAUTHORIZED = 401
PERMISSION_DENIED = 403
NOT_FOUND = 404
VALIDATION_ERROR = 422


class MCPError(Exception):
    """Base for MCP protocol / application errors."""

    def __init__(
        self,
        message: str,
        code: int = INTERNAL_ERROR,
        data: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data or {}


class UnauthorizedError(MCPError):
    """Invalid or missing API key."""

    def __init__(self, message: str = "Unauthorized: invalid or missing API key") -> None:
        super().__init__(message, code=UNAUTHORIZED)


class PermissionDeniedError(MCPError):
    """Caller does not have permission for this tool."""

    def __init__(self, message: str = "Permission denied for this tool") -> None:
        super().__init__(message, code=PERMISSION_DENIED, data={"scope": "tool"})


class InvalidInputError(MCPError):
    """Invalid tool arguments or request params."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, code=INVALID_PARAMS, data=details or {})


class ToolNotFoundError(MCPError):
    """Unknown tool name."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Unknown tool: {name}", code=NOT_FOUND, data={"tool": name})


class DestructiveConfirmationError(MCPError):
    """Destructive tool called without confirmation."""

    def __init__(self, tool_name: str) -> None:
        super().__init__(
            f"Destructive tool '{tool_name}' requires confirmation (arguments.confirm = true)",
            code=VALIDATION_ERROR,
            data={"tool": tool_name, "required": "confirm"},
        )


def json_rpc_error(code: int, message: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build a JSON-RPC 2.0 error object."""
    out: dict[str, Any] = {"code": code, "message": message}
    if data:
        out["data"] = data
    return out


def from_exception(exc: Exception) -> dict[str, Any]:
    """Turn an MCPError or generic Exception into a JSON-RPC error object."""
    if isinstance(exc, MCPError):
        return json_rpc_error(exc.code, exc.message, exc.data)
    return json_rpc_error(INTERNAL_ERROR, str(exc))

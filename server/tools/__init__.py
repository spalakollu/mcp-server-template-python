"""MCP tool registry: read, write, destructive categories."""

from __future__ import annotations

from typing import Any

from server.tools.read import TOOLS as READ_TOOLS
from server.tools.write import TOOLS as WRITE_TOOLS
from server.tools.destructive import TOOLS as DESTRUCTIVE_TOOLS

# Flatten into name -> tool def
_ALL: list[dict[str, Any]] = READ_TOOLS + WRITE_TOOLS + DESTRUCTIVE_TOOLS
REGISTRY: dict[str, dict[str, Any]] = {t["name"]: t for t in _ALL}


def list_tools() -> list[dict[str, Any]]:
    """Return MCP tool list (name, description, inputSchema only)."""
    return [
        {
            "name": t["name"],
            "description": t["description"],
            "inputSchema": t["inputSchema"],
        }
        for t in _ALL
    ]


def get_tool(name: str) -> dict[str, Any] | None:
    """Get tool definition by name, or None."""
    return REGISTRY.get(name)


def call_tool(name: str, arguments: dict[str, Any], require_scope: Any) -> dict[str, Any]:
    """
    Resolve tool, check scope, run handler. Returns MCP result (content, isError).
    require_scope is a callable(scope) that raises if not allowed.
    """
    tool = get_tool(name)
    if not tool:
        from server.errors import ToolNotFoundError
        raise ToolNotFoundError(name)

    require_scope(tool["scope"])
    handler = tool["handler"]
    return handler(arguments)

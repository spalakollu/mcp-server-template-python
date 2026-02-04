"""Production-ready MCP server over HTTP (Flask)."""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from flask import Flask, request, g

from server.errors import (
    MCPError,
    UnauthorizedError,
    METHOD_NOT_FOUND,
    INVALID_REQUEST,
    from_exception,
    json_rpc_error,
)
from server.permissions import authenticate_request, require_scope
from server.tools import list_tools, call_tool

# Structured logging: JSON-like format for tool invocations
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("mcp.server")

app = Flask(__name__)


def _log_tool_invocation(
    name: str,
    arguments: dict[str, Any],
    result: dict[str, Any] | None,
    error: str | None,
    duration_ms: float,
) -> None:
    """Structured log for each tool call."""
    payload = {
        "event": "tool_invocation",
        "tool": name,
        "arguments": arguments,
        "duration_ms": round(duration_ms, 2),
    }
    if result is not None:
        payload["is_error"] = result.get("isError", False)
    if error:
        payload["error"] = error
    logger.info("tool_invocation | %s", json.dumps(payload))


@app.before_request
def _authenticate() -> tuple[str, int] | None:
    """Validate API key and set g.scopes. Skip for health/liveness. Return 401 JSON on auth failure."""
    if request.path in ("/health", "/") and request.method == "GET":
        return None
    try:
        authenticate_request()
    except UnauthorizedError as e:
        return json.dumps({"jsonrpc": "2.0", "id": None, "error": from_exception(e)}), 401
    return None


@app.route("/health", methods=["GET"])
def health() -> tuple[str, int]:
    """Liveness/readiness probe."""
    return json.dumps({"status": "ok"}), 200


@app.route("/", methods=["POST"])
@app.route("/mcp", methods=["POST"])
def mcp_endpoint() -> tuple[str, int]:
    """
    JSON-RPC 2.0 endpoint for MCP (tools/list, tools/call).
    Expects JSON body; returns JSON-RPC response with standardized errors.
    """
    if request.content_type and "application/json" not in request.content_type:
        return _response(None, INVALID_REQUEST, "Content-Type must be application/json"), 400

    try:
        body = request.get_data(as_text=True)
        if not body:
            return _response(None, INVALID_REQUEST, "Empty body"), 400
        data = json.loads(body)
    except json.JSONDecodeError as e:
        return _response(None, -32700, f"Parse error: {e}"), 400

    if not isinstance(data, dict):
        return _response(None, INVALID_REQUEST, "Request must be a JSON object"), 400

    req_id = data.get("id")
    method = data.get("method")
    params = data.get("params") or {}

    if method == "tools/list":
        result = {"tools": list_tools(), "nextCursor": None}
        return _response(req_id, result=result), 200

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments")
        if not name:
            return _response(req_id, INVALID_REQUEST, "Missing params.name"), 200
        if arguments is None:
            arguments = {}

        start = time.perf_counter()
        try:
            result = call_tool(name, arguments, require_scope)
            duration_ms = (time.perf_counter() - start) * 1000
            _log_tool_invocation(name, arguments, result, None, duration_ms)
            return _response(req_id, result=result), 200
        except MCPError as e:
            duration_ms = (time.perf_counter() - start) * 1000
            _log_tool_invocation(name, arguments, None, e.message, duration_ms)
            return _response(req_id, error=from_exception(e)), 200
        except Exception as e:
            logger.exception("tool_call_failed")
            return _response(req_id, error=from_exception(e)), 200

    return _response(req_id, METHOD_NOT_FOUND, f"Method not found: {method}"), 200


def _response(
    req_id: Any,
    result: dict[str, Any] | None = None,
    code: int | None = None,
    message: str | None = None,
    error: dict[str, Any] | None = None,
) -> str:
    """Build JSON-RPC 2.0 response."""
    out: dict[str, Any] = {"jsonrpc": "2.0", "id": req_id}
    if error is not None:
        out["error"] = error
    elif code is not None and message is not None:
        out["error"] = json_rpc_error(code, message)
    else:
        out["result"] = result
    return json.dumps(out)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)

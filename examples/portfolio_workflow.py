"""
Example workflow: Portfolio Service (mock).
Demonstrates read, write, and destructive tools via MCP JSON-RPC over HTTP.

Run the server first:
  python -m server.main

Then run this script (optionally set MCP_API_KEY and BASE_URL):
  python examples/portfolio_workflow.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

BASE_URL = os.environ.get("MCP_BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.environ.get("MCP_API_KEY", "")


def rpc(method: str, params: dict | None = None) -> dict:
    """Send a JSON-RPC request to the MCP server."""
    data = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        out = json.loads(resp.read().decode())
    if "error" in out:
        raise RuntimeError(out["error"].get("message", out["error"]))
    return out.get("result", {})


def main() -> None:
    print("Portfolio Service example workflow (read → write → destructive)\n")

    # 1. List tools
    result = rpc("tools/list")
    tools = result.get("tools", [])
    print(f"Available tools: {[t['name'] for t in tools]}\n")

    # 2. Read: get current holdings
    print("1. Read: portfolio_get_holdings")
    result = rpc("tools/call", {"name": "portfolio_get_holdings", "arguments": {}})
    content = result.get("content", [])
    for c in content:
        if c.get("type") == "text":
            print(c.get("text", ""))
    print()

    # 3. Write: add a position
    print("2. Write: portfolio_add_position (MSFT, 3 @ 400)")
    result = rpc(
        "tools/call",
        {
            "name": "portfolio_add_position",
            "arguments": {"symbol": "MSFT", "shares": 3, "avg_cost": 400},
        },
    )
    for c in result.get("content", []):
        if c.get("type") == "text":
            print(c.get("text", ""))
    print()

    # 4. Read again to see new position
    print("3. Read again: portfolio_get_holdings")
    result = rpc("tools/call", {"name": "portfolio_get_holdings", "arguments": {}})
    for c in result.get("content", []):
        if c.get("type") == "text":
            print(c.get("text", ""))
    print()

    # 5. Destructive: close all (with confirmation)
    print("4. Destructive: portfolio_close_all (confirm=true)")
    result = rpc(
        "tools/call",
        {"name": "portfolio_close_all", "arguments": {"confirm": True}},
    )
    for c in result.get("content", []):
        if c.get("type") == "text":
            print(c.get("text", ""))
    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

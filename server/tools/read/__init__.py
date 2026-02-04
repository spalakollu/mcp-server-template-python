"""Read-only tools."""

from __future__ import annotations

from typing import Any

# Mock in-memory store for Portfolio Service example (shared with write/destructive)
_portfolio_holdings: list[dict[str, Any]] = [
    {"symbol": "AAPL", "shares": 10, "avg_cost": 150.0},
    {"symbol": "GOOGL", "shares": 5, "avg_cost": 140.0},
]


def get_portfolio_holdings() -> list[dict[str, Any]]:
    """Return current portfolio holdings (mock)."""
    return [h.copy() for h in _portfolio_holdings]


def add_holding(symbol: str, shares: float, avg_cost: float) -> None:
    """Add or update a position (mock). Used by write tool."""
    for h in _portfolio_holdings:
        if h["symbol"] == symbol:
            old_shares = h["shares"]
            h["shares"] = old_shares + shares
            h["avg_cost"] = (h["avg_cost"] * old_shares + avg_cost * shares) / h["shares"]
            return
    _portfolio_holdings.append({"symbol": symbol, "shares": shares, "avg_cost": avg_cost})


def clear_holdings() -> None:
    """Clear all holdings (mock). Used by destructive tool."""
    _portfolio_holdings.clear()


def portfolio_get_holdings(_arguments: dict[str, Any]) -> dict[str, Any]:
    """
    Get current portfolio holdings (read-only).
    Part of the mock Portfolio Service example.
    """
    holdings = get_portfolio_holdings()
    lines = ["Symbol | Shares | Avg Cost"]
    for h in holdings:
        lines.append(f"{h['symbol']} | {h['shares']} | {h['avg_cost']}")
    return {
        "content": [{"type": "text", "text": "\n".join(lines)}],
        "isError": False,
    }


# Tool definitions for MCP (name, description, inputSchema, handler, scope)
TOOLS = [
    {
        "name": "portfolio_get_holdings",
        "description": "Get current portfolio holdings (read-only). Mock Portfolio Service.",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
        "handler": portfolio_get_holdings,
        "scope": "read",
        "category": "read",
    },
]

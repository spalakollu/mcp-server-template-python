"""Write-capable tools."""

from __future__ import annotations

from typing import Any

from server.errors import InvalidInputError
from server.tools.read import add_holding


def portfolio_add_position(arguments: dict[str, Any]) -> dict[str, Any]:
    """
    Add a position to the portfolio (write).
    Part of the mock Portfolio Service example.
    """
    symbol = arguments.get("symbol")
    shares = arguments.get("shares")
    avg_cost = arguments.get("avg_cost")

    if not symbol or not isinstance(symbol, str):
        raise InvalidInputError("Missing or invalid 'symbol' (string required)")
    try:
        s = float(shares) if shares is not None else None
        c = float(avg_cost) if avg_cost is not None else None
    except (TypeError, ValueError):
        raise InvalidInputError("'shares' and 'avg_cost' must be numbers")

    if s is None or s <= 0:
        raise InvalidInputError("'shares' must be a positive number")
    if c is None or c < 0:
        raise InvalidInputError("'avg_cost' must be a non-negative number")

    add_holding(symbol.strip().upper(), s, c)
    return {
        "content": [{"type": "text", "text": f"Added {s} shares of {symbol} @ {c}"}],
        "isError": False,
    }


TOOLS = [
    {
        "name": "portfolio_add_position",
        "description": "Add a position to the portfolio. Mock Portfolio Service.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Ticker symbol"},
                "shares": {"type": "number", "description": "Number of shares"},
                "avg_cost": {"type": "number", "description": "Average cost per share"},
            },
            "required": ["symbol", "shares", "avg_cost"],
        },
        "handler": portfolio_add_position,
        "scope": "write",
        "category": "write",
    },
]

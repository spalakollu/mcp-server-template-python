"""Destructive tools (require confirmation)."""

from __future__ import annotations

from typing import Any

from server.errors import DestructiveConfirmationError
from server.tools.read import clear_holdings, get_portfolio_holdings


def portfolio_close_all(arguments: dict[str, Any]) -> dict[str, Any]:
    """
    Close all portfolio positions (destructive). Requires arguments.confirm = true.
    Part of the mock Portfolio Service example.
    """
    if arguments.get("confirm") is not True:
        raise DestructiveConfirmationError("portfolio_close_all")

    count_before = len(get_portfolio_holdings())
    clear_holdings()
    return {
        "content": [
            {
                "type": "text",
                "text": f"Closed all positions ({count_before} holdings cleared).",
            }
        ],
        "isError": False,
    }


TOOLS = [
    {
        "name": "portfolio_close_all",
        "description": "Close all portfolio positions. Destructive; requires confirm: true.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "confirm": {
                    "type": "boolean",
                    "description": "Must be true to execute this destructive action",
                },
            },
            "required": ["confirm"],
        },
        "handler": portfolio_close_all,
        "scope": "destructive",
        "category": "destructive",
    },
]

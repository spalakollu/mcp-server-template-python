"""Minimal test stubs for MCP tools."""

import pytest

from server.tools.read import portfolio_get_holdings, get_portfolio_holdings, add_holding, clear_holdings
from server.tools.write import portfolio_add_position
from server.tools.destructive import portfolio_close_all
from server.errors import DestructiveConfirmationError, InvalidInputError


class TestReadTools:
    """Stubs for read-only tools."""

    def setup_method(self) -> None:
        clear_holdings()
        add_holding("AAPL", 10.0, 150.0)
        add_holding("GOOGL", 5.0, 140.0)

    def test_portfolio_get_holdings_returns_content(self) -> None:
        result = portfolio_get_holdings({})
        assert "content" in result
        assert result.get("isError") is False
        text = result["content"][0]["text"]
        assert "AAPL" in text and "GOOGL" in text


class TestWriteTools:
    """Stubs for write tools."""

    def setup_method(self) -> None:
        clear_holdings()

    def test_portfolio_add_position_success(self) -> None:
        result = portfolio_add_position({"symbol": "MSFT", "shares": 2, "avg_cost": 300})
        assert result.get("isError") is False
        assert get_portfolio_holdings()[0]["symbol"] == "MSFT"

    def test_portfolio_add_position_invalid_symbol(self) -> None:
        with pytest.raises(InvalidInputError):
            portfolio_add_position({"symbol": "", "shares": 1, "avg_cost": 100})


class TestDestructiveTools:
    """Stubs for destructive tools."""

    def setup_method(self) -> None:
        clear_holdings()
        add_holding("AAPL", 1.0, 100.0)

    def test_portfolio_close_all_requires_confirm(self) -> None:
        with pytest.raises(DestructiveConfirmationError):
            portfolio_close_all({"confirm": False})

    def test_portfolio_close_all_with_confirm(self) -> None:
        result = portfolio_close_all({"confirm": True})
        assert result.get("isError") is False
        assert len(get_portfolio_holdings()) == 0

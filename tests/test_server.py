"""Minimal test stubs for Flask MCP server."""

import json

import pytest

from server.main import app


@pytest.fixture
def client() -> "Flask.test_client":
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client: "Flask.test_client") -> None:
    r = client.get("/health")
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data.get("status") == "ok"


def test_tools_list(client: "Flask.test_client") -> None:
    r = client.post(
        "/",
        data=json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}),
        content_type="application/json",
    )
    assert r.status_code == 200
    data = json.loads(r.data)
    assert "result" in data
    tools = data["result"].get("tools", [])
    names = [t["name"] for t in tools]
    assert "portfolio_get_holdings" in names
    assert "portfolio_add_position" in names
    assert "portfolio_close_all" in names


def test_tools_call_read(client: "Flask.test_client") -> None:
    r = client.post(
        "/",
        data=json.dumps({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "portfolio_get_holdings", "arguments": {}},
        }),
        content_type="application/json",
    )
    assert r.status_code == 200
    data = json.loads(r.data)
    assert "result" in data
    assert data["result"].get("isError") is False
    assert len(data["result"].get("content", [])) >= 1

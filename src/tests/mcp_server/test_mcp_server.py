from __future__ import annotations

import mcp_server as mcp_server_module


def test_create_fastmcp_server_with_auth(monkeypatch):
    created = {}

    def fake_create_mcp_server(name, auth=None):
        created["name"] = name
        created["auth"] = auth
        return "server"

    def fake_jwt(**kwargs):
        return {"jwt": kwargs}

    monkeypatch.setattr(mcp_server_module, "JWTVerifier", fake_jwt)
    monkeypatch.setattr(mcp_server_module.factory, "create_mcp_server", fake_create_mcp_server)
    monkeypatch.setattr(mcp_server_module.config, "enable_auth", True)
    monkeypatch.setattr(mcp_server_module.config, "jwks_uri", "jwks")
    monkeypatch.setattr(mcp_server_module.config, "issuer", "issuer")
    monkeypatch.setattr(mcp_server_module.config, "audience", "aud")
    monkeypatch.setattr(mcp_server_module.config, "server_name", "Server")

    server = mcp_server_module.create_fastmcp_server()
    assert server == "server"
    assert created["name"] == "Server"
    assert created["auth"]["jwt"]["jwks_uri"] == "jwks"


def test_create_fastmcp_server_without_auth(monkeypatch):
    monkeypatch.setattr(mcp_server_module.factory, "create_mcp_server", lambda **_k: "server")
    monkeypatch.setattr(mcp_server_module.config, "enable_auth", False)

    server = mcp_server_module.create_fastmcp_server()
    assert server == "server"


def test_run_server_http_transport(monkeypatch):
    calls = {}

    class FakeMCP:
        def run(self, **kwargs):
            calls.update(kwargs)

    monkeypatch.setattr(mcp_server_module, "mcp", FakeMCP())

    mcp_server_module.run_server(transport="http", host="0.0.0.0", port=9000, log_level="info")
    assert calls["transport"] == "http"
    assert calls["host"] == "0.0.0.0"
    assert calls["port"] == 9000


def test_run_server_stdio_transport(monkeypatch):
    calls = {}

    class FakeMCP:
        def run(self, **kwargs):
            calls.update(kwargs)

    monkeypatch.setattr(mcp_server_module, "mcp", FakeMCP())

    mcp_server_module.run_server(transport="stdio", log_level="info", extra="ok")
    assert calls["transport"] == "stdio"
    assert "log_level" not in calls
    assert calls["extra"] == "ok"

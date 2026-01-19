from __future__ import annotations

from config.settings import config, get_auth_config, get_server_config


def test_get_auth_config_disabled(monkeypatch):
    monkeypatch.setattr(config, "enable_auth", False)
    assert get_auth_config() is None


def test_get_auth_config_enabled(monkeypatch):
    monkeypatch.setattr(config, "enable_auth", True)
    monkeypatch.setattr(config, "tenant_id", "tenant")
    monkeypatch.setattr(config, "client_id", "client")
    monkeypatch.setattr(config, "jwks_uri", "jwks")
    monkeypatch.setattr(config, "issuer", "issuer")
    monkeypatch.setattr(config, "audience", "aud")

    auth = get_auth_config()
    assert auth["tenant_id"] == "tenant"
    assert auth["client_id"] == "client"
    assert auth["jwks_uri"] == "jwks"
    assert auth["issuer"] == "issuer"
    assert auth["audience"] == "aud"


def test_get_server_config(monkeypatch):
    monkeypatch.setattr(config, "host", "0.0.0.0")
    monkeypatch.setattr(config, "port", 1234)
    monkeypatch.setattr(config, "debug", True)

    server = get_server_config()
    assert server == {"host": "0.0.0.0", "port": 1234, "debug": True}

from __future__ import annotations

from typing import List

import core.factory as factory_module
from core.factory import MCPToolBase, MCPToolFactory, Domain


class DummyMCP:
    def __init__(self, name, auth=None):
        self.name = name
        self.auth = auth
        self.tools: List[str] = []


class DummyService(MCPToolBase):
    def __init__(self, domain: Domain, tool_count: int = 1):
        super().__init__(domain)
        self._tool_count = tool_count
        self.registered = False

    @property
    def tool_count(self) -> int:
        return self._tool_count

    def register_tools(self, mcp) -> None:
        self.registered = True


def test_factory_register_and_summary():
    factory = MCPToolFactory()
    service = DummyService(Domain.GENERAL, tool_count=2)
    factory.register_service(service)

    summary = factory.get_tool_summary()
    assert summary["total_services"] == 1
    assert summary["total_tools"] == 2
    assert summary["services"]["general"]["tool_count"] == 2


def test_factory_create_mcp_server_registers_tools(monkeypatch):
    factory = MCPToolFactory()
    service = DummyService(Domain.DEMO)
    factory.register_service(service)

    monkeypatch.setattr(factory_module, "FastMCP", DummyMCP)

    mcp = factory.create_mcp_server(name="Test", auth=None)
    assert isinstance(mcp, DummyMCP)
    assert service.registered is True

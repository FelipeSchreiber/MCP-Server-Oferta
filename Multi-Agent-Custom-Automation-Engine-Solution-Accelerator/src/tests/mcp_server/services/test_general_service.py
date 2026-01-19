from __future__ import annotations

from services.demo_general_service import GeneralService


class FakeMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, **_kwargs):
        def decorator(fn):
            self.tools[fn.__name__] = fn
            return fn

        return decorator


def test_general_service_registers_tools():
    mcp = FakeMCP()
    service = GeneralService()
    service.register_tools(mcp)

    assert "greet_test" in mcp.tools
    assert "get_server_status" in mcp.tools


def test_general_service_greet_tool_returns_success():
    mcp = FakeMCP()
    service = GeneralService()
    service.register_tools(mcp)

    result = mcp.tools["greet_test"]("Alice")
    assert "Greeting Completed" in result
    assert "Hello from BB MCP Server, Alice" in result

from __future__ import annotations

import pytest

from services.demo_general_service import GeneralService


class FakeMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, **_kwargs):
        def decorator(fn):
            self.tools[fn.__name__] = fn
            return fn

        return decorator


@pytest.mark.asyncio
async def test_general_service_uses_formatters():
    mcp = FakeMCP()
    service = GeneralService()
    service.register_tools(mcp)

    result = await mcp.tools["get_server_status"]()
    assert "Server Status Completed" in result
    assert "BB MCP Server" in result

from __future__ import annotations

import pytest

from services.bb_demo_service import BBDemoService


class FakeActionResult:
    def __init__(self, action: str):
        self.action = action


class FakeContext:
    def __init__(self, action: str):
        self._action = action

    async def elicit(self, _prompt: str):
        return FakeActionResult(self._action)


class FakeMCP:
    def __init__(self):
        self.tools = {}
        self.resources = {}
        self.prompts = []

    def tool(self, **_kwargs):
        def decorator(fn):
            self.tools[_kwargs.get("name", fn.__name__)] = fn
            return fn

        return decorator

    def resource(self, uri, **_kwargs):
        def decorator(fn):
            self.resources[uri] = fn
            return fn

        return decorator

    def prompt(self, fn):
        self.prompts.append(fn)
        return fn


def test_demo_service_registers_tools_resources_prompts():
    mcp = FakeMCP()
    service = BBDemoService()
    service.register_tools(mcp)

    assert "add_two_numbers" in mcp.tools
    assert "get_user_info" in mcp.tools
    assert "config://app_config" in mcp.resources
    assert "users://{user_id}/telephone" in mcp.resources
    assert len(mcp.prompts) == 1


def test_demo_service_add_two_numbers():
    mcp = FakeMCP()
    service = BBDemoService()
    service.register_tools(mcp)

    assert mcp.tools["add_two_numbers"](2, 3) == 5


@pytest.mark.asyncio
async def test_demo_service_get_user_info_accept():
    mcp = FakeMCP()
    service = BBDemoService()
    service.register_tools(mcp)

    ctx = FakeContext("accept")
    result = await mcp.tools["get_user_info"](ctx, user_id=1)
    assert result["id"] == 1
    assert result["status"] == "active"


@pytest.mark.asyncio
async def test_demo_service_get_user_info_decline():
    mcp = FakeMCP()
    service = BBDemoService()
    service.register_tools(mcp)

    ctx = FakeContext("decline")
    result = await mcp.tools["get_user_info"](ctx, user_id=1)
    assert result["message"] == "Declined!"

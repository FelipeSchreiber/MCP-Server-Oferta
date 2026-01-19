from __future__ import annotations

import pytest

from services.tech_support_service import TechSupportService


class FakeMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, **_kwargs):
        def decorator(fn):
            self.tools[fn.__name__] = fn
            return fn

        return decorator


@pytest.mark.asyncio
async def test_tech_support_registers_tools_and_run():
    mcp = FakeMCP()
    service = TechSupportService()
    service.register_tools(mcp)

    assert "send_welcome_email" in mcp.tools
    assert "set_up_office_365_account" in mcp.tools
    assert "configure_laptop" in mcp.tools
    assert "setup_vpn_access" in mcp.tools

    result = await mcp.tools["send_welcome_email"](
        employee_name="Sam", email_address="sam@example.com"
    )
    assert "Welcome Email Sent" in result
    assert "sam@example.com" in result

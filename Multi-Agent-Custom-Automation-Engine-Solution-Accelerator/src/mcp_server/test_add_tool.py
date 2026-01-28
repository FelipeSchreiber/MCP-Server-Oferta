#!/usr/bin/env python3
"""Simple test script for add_two_numbers MCP tool."""

import asyncio
import httpx
import json


def parse_sse_response(text: str):
    """Parse Server-Sent Events response and extract JSON data."""
    lines = text.strip().split('\n')
    for line in lines:
        if line.startswith('data: '):
            data_str = line[6:]  # Remove 'data: ' prefix
            try:
                return json.loads(data_str)
            except json.JSONDecodeError:
                continue
    return None


async def test_add_two_numbers():
    """Test the add_two_numbers tool via MCP HTTP endpoint."""

    # MCP server URL
    url = "http://localhost:9000/mcp"

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Initialize session
        print("🔄 Initializing MCP session...")
        init_response = await client.post(
            url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        )

        print(f"📋 Init Response: {init_response.status_code}")
        if init_response.status_code == 200:
            # For SSE responses, content might be empty or event-stream format
            try:
                response_data = init_response.json()
                print(f"✅ {response_data}")
            except Exception:
                print("✅ Connected (SSE stream)")
                print(f"   Response text: {init_response.text[:200]}")
        else:
            print(f"❌ {init_response.text}")
            return

        # Get session ID from headers
        session_id = init_response.headers.get("mcp-session-id")
        print(f"🔑 Session ID: {session_id}")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if session_id:
            headers["mcp-session-id"] = session_id

        # List available tools
        print("\n🔄 Listing available tools...")
        tools_response = await client.post(
            url,
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            },
            headers=headers
        )

        print(f"📋 Tools Response: {tools_response.status_code}")
        if tools_response.status_code == 200:
            tools_data = parse_sse_response(tools_response.text)
            if tools_data:
                print("✅ Available tools:")
                for tool in tools_data.get("result", {}).get("tools", []):
                    print(f"   - {tool.get('name')}: {tool.get('description')}")
            else:
                print(f"⚠️  Could not parse response: {tools_response.text[:200]}")
        else:
            print(f"❌ {tools_response.text}")

        # Call add_two_numbers tool
        print("\n🔄 Calling add_two_numbers(5, 3)...")
        call_response = await client.post(
            url,
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "add_two_numbers",
                    "arguments": {
                        "a": 5,
                        "b": 3
                    }
                }
            },
            headers=headers
        )

        print(f"📋 Call Response: {call_response.status_code}")
        if call_response.status_code == 200:
            result = parse_sse_response(call_response.text)
            if result:
                print(f"✅ Result: {result}")
                content = result.get("result", {}).get("content", [])
                if content:
                    print(f"🎯 Answer: {content[0].get('text')}")
            else:
                print(f"⚠️  Could not parse response: {call_response.text[:200]}")
        else:
            print(f"❌ {call_response.text}")


if __name__ == "__main__":
    print("🚀 Testing add_two_numbers MCP tool\n")
    asyncio.run(test_add_two_numbers())
    print("\n✨ Test complete!")

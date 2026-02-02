"""Test script for MCP agent - Docker version."""

import asyncio
import logging
import os
from agent import MCPAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_mcp_agent():
    """Test the MCP agent with a running MCP server."""
    
    print("\n" + "="*60)
    print("🧪 Testing MCP Agent (Docker)")
    print("="*60 + "\n")
    
    # Use Docker service name for MCP server
    mcp_url = os.getenv("MCP_SERVER_URL", "http://mcp-server:9000/mcp")
    
    # Initialize agent with MCP server
    agent = MCPAgent(
        name="test_agent",
        mcp_servers=[mcp_url]
    )
    
    print(f"✅ Agent initialized with {len(agent.tools)} tools\n")
    
    # Test 1: Simple calculation
    print("📝 Test 1: Calculate 15 + 27\n")
    try:
        result1 = await agent.run(
            task="Add the numbers 15 and 27",
            session_id="test_session_1"
        )
        print(f"✅ Result: {result1['output']}\n")
    except Exception as e:
        print(f"❌ Test 1 failed: {e}\n")
    
    # Test 2: Get current date
    print("📝 Test 2: Get current date\n")
    try:
        result2 = await agent.run(
            task="What is the current date?",
            session_id="test_session_2"
        )
        print(f"✅ Result: {result2['output']}\n")
    except Exception as e:
        print(f"❌ Test 2 failed: {e}\n")
    
    print("="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("\n🚀 Starting MCP Agent Tests (Docker)\n")
    
    try:
        asyncio.run(test_mcp_agent())
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)

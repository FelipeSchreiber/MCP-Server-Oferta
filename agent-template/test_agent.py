"""Test script for MCP agent."""

import asyncio
import logging
from agent import MCPAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_mcp_agent():
    """Test the MCP agent with a running MCP server."""
    
    print("\n" + "="*60)
    print("🧪 Testing MCP Agent")
    print("="*60 + "\n")
    
    # Initialize agent with MCP server
    # Make sure your MCP server is running at http://localhost:9000/mcp
    agent = MCPAgent(
        name="test_agent",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    
    print(f"✅ Agent initialized with {len(agent.tools)} tools\n")
    
    # Test 1: Simple calculation
    print("📝 Test 1: Calculate 15 + 27\n")
    result1 = await agent.run(
        task="Add the numbers 15 and 27",
        session_id="test_session_1"
    )
    print(f"✅ Result: {result1['output']}\n")
    
    # Test 2: Get current date
    print("📝 Test 2: Get current date\n")
    result2 = await agent.run(
        task="What is the current date?",
        session_id="test_session_2"
    )
    print(f"✅ Result: {result2['output']}\n")
    
    # Test 3: Format text
    print("📝 Test 3: Format text to uppercase\n")
    result3 = await agent.run(
        task="Format the text 'hello world' to uppercase",
        session_id="test_session_3"
    )
    print(f"✅ Result: {result3['output']}\n")
    
    print("="*60)
    print("✅ All tests completed!")
    print("="*60 + "\n")


async def test_with_memory():
    """Test agent with memory persistence."""
    
    print("\n" + "="*60)
    print("🧪 Testing MCP Agent with Memory")
    print("="*60 + "\n")
    
    agent = MCPAgent(
        name="memory_test_agent",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    
    session_id = "memory_test_session"
    
    # First interaction
    print("📝 Interaction 1: Calculate 5 + 10\n")
    result1 = await agent.run(
        task="Calculate 5 plus 10",
        session_id=session_id
    )
    print(f"✅ Response: {result1['output']}\n")
    
    # Second interaction (should have context)
    print("📝 Interaction 2: Double the previous result\n")
    result2 = await agent.run(
        task="Double the previous result",
        session_id=session_id
    )
    print(f"✅ Response: {result2['output']}\n")
    
    # Check session history
    history = agent.memory.get_session_history(session_id)
    print(f"📚 Session history: {len(history)} interactions\n")
    for i, interaction in enumerate(history, 1):
        print(f"{i}. [{interaction['role']}] {interaction['content'][:100]}...")


async def test_multiple_servers():
    """Test agent with multiple MCP servers."""
    
    print("\n" + "="*60)
    print("🧪 Testing MCP Agent with Multiple Servers")
    print("="*60 + "\n")
    
    # You can add more MCP server URLs here
    agent = MCPAgent(
        name="multi_server_agent",
        mcp_servers=[
            "http://localhost:9000/mcp",
            # "http://localhost:9001/mcp",  # Add more servers
        ]
    )
    
    print(f"✅ Agent connected to {len(agent.mcp_servers)} MCP servers")
    print(f"✅ Total tools available: {len(agent.tools)}\n")
    
    result = await agent.run(
        task="Add 100 and 200",
        session_id="multi_server_test"
    )
    
    print(f"✅ Result: {result['output']}\n")


if __name__ == "__main__":
    print("\n🚀 Starting MCP Agent Tests\n")
    print("⚠️  Make sure your MCP server is running at http://localhost:9000/mcp\n")
    
    try:
        # Test 1: Basic functionality
        asyncio.run(test_mcp_agent())
        
        # Test 2: Memory persistence (uncomment to test)
        # asyncio.run(test_with_memory())
        
        # Test 3: Multiple servers (uncomment to test)
        # asyncio.run(test_multiple_servers())
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        print("Make sure:")
        print("1. MongoDB is running (docker-compose up in /memory folder)")
        print("2. MCP server is running at http://localhost:9000/mcp")
        print("3. OPENAI_API_KEY is set in .env file\n")

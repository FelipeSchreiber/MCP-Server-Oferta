"""Integration test: Orchestrator coordinating multiple MCP agents."""

import asyncio
import logging
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "orchestrator-agent"))
sys.path.insert(0, str(Path(__file__).parent / "agent-template"))

from orchestrator import OrchestratorAgent
from agent import MCPAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_integration():
    """Test orchestrator coordinating MCP agents."""
    
    print("\n" + "="*70)
    print("🧪 INTEGRATION TEST: Orchestrator + MCP Agents")
    print("="*70 + "\n")
    
    # Create MCP agents
    print("🤖 Creating specialized MCP agents...\n")
    
    math_agent = MCPAgent(
        name="math_agent",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    print(f"✅ Math Agent ready with {len(math_agent.tools)} tools")
    
    support_agent = MCPAgent(
        name="support_agent",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    print(f"✅ Support Agent ready with {len(support_agent.tools)} tools\n")
    
    # Create orchestrator
    print("🎯 Creating orchestrator...\n")
    orchestrator = OrchestratorAgent()
    print("✅ Orchestrator ready\n")
    
    # Complex task requiring coordination
    complex_task = """
    I need you to:
    1. Calculate the sum of 25 and 75
    2. Check the system status
    3. Format the calculation result as uppercase text
    4. Get the current date
    """
    
    print("="*70)
    print(f"📝 Complex Task:\n{complex_task}")
    print("="*70 + "\n")
    
    # Run orchestrator (it will coordinate the agents)
    print("🚀 Starting orchestration...\n")
    
    result = await orchestrator.run(task=complex_task)
    
    print("\n" + "="*70)
    print("✅ INTEGRATION TEST RESULTS")
    print("="*70)
    
    print(f"\n📊 Final Output:\n{result['final_output']}\n")
    
    print("📈 Execution Details:")
    print(f"  - Session ID: {result['session_id']}")
    print(f"  - Total Steps: {len(result.get('steps', []))}")
    print(f"  - Math Agent Tools: {len(math_agent.tools)}")
    print(f"  - Support Agent Tools: {len(support_agent.tools)}")
    
    print("\n🎉 Integration test completed successfully!\n")


async def test_agent_collaboration():
    """Test multiple agents working on different parts of a task."""
    
    print("\n" + "="*70)
    print("🧪 AGENT COLLABORATION TEST")
    print("="*70 + "\n")
    
    # Create agents with different responsibilities
    calculator = MCPAgent(
        name="calculator",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    
    formatter = MCPAgent(
        name="formatter",
        mcp_servers=["http://localhost:9000/mcp"]
    )
    
    # Shared session for context
    session_id = "collaboration_session"
    
    # Agent 1: Do calculation
    print("🤖 Agent 1 (Calculator): Adding 50 + 30\n")
    calc_result = await calculator.run(
        task="Add 50 and 30",
        session_id=session_id
    )
    print(f"✅ Calculation result: {calc_result['output']}\n")
    
    # Agent 2: Format the result
    print("🤖 Agent 2 (Formatter): Formatting the result\n")
    format_result = await formatter.run(
        task=f"Format the text '{calc_result['output']}' to uppercase",
        session_id=session_id
    )
    print(f"✅ Formatted result: {format_result['output']}\n")
    
    # Check shared memory
    history = calculator.memory.get_session_history(session_id)
    print(f"📚 Shared session history: {len(history)} interactions")
    
    print("\n🎉 Collaboration test completed!\n")


if __name__ == "__main__":
    print("\n🚀 Starting Integration Tests\n")
    print("⚠️  Prerequisites:")
    print("   1. MongoDB running: cd memory && docker-compose up -d")
    print("   2. MCP server running at http://localhost:9000/mcp")
    print("   3. OPENAI_API_KEY set in both .env files\n")
    
    try:
        # Test 1: Full integration
        asyncio.run(test_integration())
        
        # Test 2: Agent collaboration
        # asyncio.run(test_agent_collaboration())
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}\n")
        import traceback
        traceback.print_exc()
        print("\nTroubleshooting:")
        print("1. Check MongoDB is running: docker ps | grep mongo")
        print("2. Check MCP server: curl http://localhost:9000/mcp")
        print("3. Check .env files have OPENAI_API_KEY\n")

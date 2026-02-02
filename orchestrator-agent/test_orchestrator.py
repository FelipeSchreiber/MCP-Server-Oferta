"""Test script for orchestrator agent."""

import asyncio
import logging
from orchestrator import OrchestratorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_orchestrator():
    """Test the orchestrator agent."""
    
    print("\n" + "="*60)
    print("🧪 Testing Orchestrator Agent")
    print("="*60 + "\n")
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(
        model="gpt-4-turbo-preview"
    )
    
    # Test with a simple task
    test_task = "Calculate the sum of 15 and 27, then format the result as uppercase text"
    
    print(f"📝 Task: {test_task}\n")
    
    # Run orchestrator
    result = await orchestrator.run(task=test_task)
    
    print("\n" + "="*60)
    print("✅ Test Results")
    print("="*60)
    print(f"\nFinal Output:\n{result['final_output']}")
    print(f"\nSession ID: {result['session_id']}")
    print(f"Steps Executed: {len(result.get('steps', []))}")
    print("\nMetadata:")
    for key, value in result.get('metadata', {}).items():
        print(f"  - {key}: {value}")


async def test_with_memory():
    """Test orchestrator with memory persistence."""
    
    print("\n" + "="*60)
    print("🧪 Testing Orchestrator with Memory")
    print("="*60 + "\n")
    
    orchestrator = OrchestratorAgent()
    
    session_id = "test_session_123"
    
    # First interaction
    print("📝 Task 1: What is 10 plus 20?\n")
    result1 = await orchestrator.run(
        task="What is 10 plus 20?",
        session_id=session_id
    )
    print(f"✅ Response 1: {result1['final_output']}\n")
    
    # Second interaction (should have context)
    print("📝 Task 2: Now multiply that by 2\n")
    result2 = await orchestrator.run(
        task="Now multiply that by 2",
        session_id=session_id
    )
    print(f"✅ Response 2: {result2['final_output']}\n")
    
    # Check session history
    history = orchestrator.memory.get_session_history(session_id)
    print(f"\n📚 Session history has {len(history)} interactions")


if __name__ == "__main__":
    print("\n🚀 Starting Orchestrator Tests\n")
    
    # Test 1: Basic orchestration
    asyncio.run(test_orchestrator())
    
    # Test 2: Memory persistence
    # asyncio.run(test_with_memory())  # Uncomment to test memory
    
    print("\n✅ All tests completed!\n")

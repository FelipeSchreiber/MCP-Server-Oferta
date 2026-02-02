"""Test script for orchestrator agent - Docker version."""

import asyncio
import logging
from orchestrator import OrchestratorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_orchestrator():
    """Test the orchestrator agent."""
    
    print("\n" + "="*60)
    print("🧪 Testing Orchestrator Agent (Docker)")
    print("="*60 + "\n")
    
    # Initialize orchestrator
    try:
        orchestrator = OrchestratorAgent()
        print("✅ Orchestrator initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize orchestrator: {e}\n")
        return
    
    # Test with a simple task
    test_task = "Create a plan to calculate 15 + 27 and explain the result"
    
    # Mock agent configs
    agent_configs = [
        {"name": "math_agent", "type": "calculator", "capabilities": ["arithmetic"]},
        {"name": "analysis_agent", "type": "analyzer", "capabilities": ["explanation"]}
    ]
    
    print(f"📝 Task: {test_task}\n")
    
    # Run orchestrator
    try:
        result = await orchestrator.run(
            task=test_task,
            agent_configs=agent_configs
        )
        
        print("\n" + "="*60)
        print("✅ Test Results")
        print("="*60)
        print(f"\nFinal Output:\n{result['final_output']}")
        print(f"\nSession ID: {result['session_id']}")
        print(f"Steps Executed: {len(result.get('steps', []))}")
        
    except Exception as e:
        print(f"\n❌ Orchestrator test failed: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    print("\n🚀 Starting Orchestrator Tests (Docker)\n")
    
    try:
        asyncio.run(test_orchestrator())
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        exit(1)

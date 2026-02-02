"""Quick test of orchestrator with calculation question."""

import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, '/app' if os.path.exists('/app/orchestrator.py') else '.')

from orchestrator import OrchestratorAgent


async def main():
    print("\n" + "="*70)
    print("🧪 Testing Orchestrator: What is the result of 6 + 999?")
    print("="*70 + "\n")
    
    # Initialize orchestrator
    try:
        orchestrator = OrchestratorAgent()
        print("✅ Orchestrator initialized\n")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}\n")
        return
    
    # Mock agent configs
    agent_configs = [
        {"name": "math_agent", "type": "calculator", "capabilities": ["arithmetic", "math"]},
        {"name": "general_agent", "type": "general", "capabilities": ["reasoning", "explanation"]}
    ]
    
    # The question
    question = "what is the result of 6 + 999?"
    print(f"📝 Question: {question}\n")
    print("🔄 Processing...\n")
    
    try:
        result = await orchestrator.run(
            task=question,
            agent_configs=agent_configs
        )
        
        print("="*70)
        print("✅ ORCHESTRATOR RESPONSE")
        print("="*70)
        print(f"\n{result['final_output']}\n")
        print("="*70)
        print(f"Session ID: {result['session_id']}")
        print(f"Status: {result.get('current_step', 'completed')}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

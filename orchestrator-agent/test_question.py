import asyncio
from orchestrator import OrchestratorAgent

async def main():
    print("\n" + "="*70)
    print("🧪 Testing Orchestrator: What is the result of 6 + 999?")
    print("="*70 + "\n")
    
    orchestrator = OrchestratorAgent()
    print("✅ Orchestrator initialized\n")
    
    agent_configs = [
        {"name": "math_agent", "type": "calculator", "capabilities": ["arithmetic", "math"]},
        {"name": "general_agent", "type": "general", "capabilities": ["reasoning"]}
    ]
    
    question = "what is the result of 6 + 999?"
    print(f"📝 Question: {question}\n")
    print("🔄 Processing...\n")
    
    result = await orchestrator.run(
        task=question,
        agent_configs=agent_configs
    )
    
    print("="*70)
    print("✅ ORCHESTRATOR RESPONSE")
    print("="*70)
    print(f"\n{result['output']}\n")
    print("="*70)
    print(f"Session ID: {result['session_id']}")
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(main())

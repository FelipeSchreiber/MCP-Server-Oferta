"""Orchestrator Agent using LangGraph for multi-agent coordination."""

import logging
from typing import TypedDict, Annotated, Sequence, Literal
from operator import add
from datetime import datetime

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pymongo import MongoClient

from config import settings
from memory import MongoMemory

logger = logging.getLogger(__name__)


class OrchestratorState(TypedDict):
    """State for the orchestrator agent."""
    messages: Annotated[Sequence[BaseMessage], add]
    task: str
    plan: str
    agent_configs: list[dict]
    agent_results: dict[str, any]
    final_output: str
    current_step: str


class OrchestratorAgent:
    """Orchestrator agent that coordinates multiple specialized agents."""
    
    def __init__(self, mongo_uri: str = None):
        """Initialize the orchestrator agent.
        
        Args:
            mongo_uri: MongoDB connection URI
        """
        self.mongo_uri = mongo_uri or settings.mongodb_uri
        self.memory = MongoMemory(self.mongo_uri)
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
        self.graph = self._create_graph()
        
        logger.info("✅ Orchestrator agent initialized")
    
    def _create_graph(self) -> StateGraph:
        """Create the LangGraph workflow."""
        workflow = StateGraph(OrchestratorState)
        
        # Add nodes
        workflow.add_node("analyze", self._analyze_task)
        workflow.add_node("plan", self._create_plan)
        workflow.add_node("delegate", self._delegate_to_agents)
        workflow.add_node("aggregate", self._aggregate_results)
        workflow.add_node("finalize", self._finalize_output)
        
        # Add edges
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "plan")
        workflow.add_edge("plan", "delegate")
        workflow.add_edge("delegate", "aggregate")
        workflow.add_edge("aggregate", "finalize")
        workflow.add_edge("finalize", END)
        
        return workflow.compile()
    
    async def _analyze_task(self, state: OrchestratorState) -> dict:
        """Analyze the incoming task."""
        logger.info(f"📋 Analyzing task: {state['task']}")
        
        messages = [
            HumanMessage(content=f"""Analyze this task and identify what needs to be done:
            
Task: {state['task']}

Available agents: {[agent['name'] for agent in state.get('agent_configs', [])]}

Provide a brief analysis of what this task requires.""")
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "messages": state["messages"] + [response],
            "current_step": "analyzed"
        }
    
    async def _create_plan(self, state: OrchestratorState) -> dict:
        """Create an execution plan."""
        logger.info("🗺️ Creating execution plan")
        
        messages = state["messages"] + [
            HumanMessage(content=f"""Based on the task analysis, create a step-by-step plan for completing:

Task: {state['task']}
Available agents: {[agent['name'] for agent in state.get('agent_configs', [])]}

Create a detailed execution plan assigning specific steps to agents.""")
        ]
        
        response = await self.llm.ainvoke(messages)
        plan = response.content
        
        # Store plan in memory
        self.memory.save_interaction(
            session_id=state.get("session_id", "default"),
            role="orchestrator",
            content=f"Plan: {plan}",
            metadata={"task": state["task"], "timestamp": datetime.utcnow().isoformat()}
        )
        
        return {
            "messages": state["messages"] + [response],
            "plan": plan,
            "current_step": "planned"
        }
    
    async def _delegate_to_agents(self, state: OrchestratorState) -> dict:
        """Delegate work to specialized agents."""
        logger.info("🚀 Delegating to agents")
        
        # In a real implementation, this would call actual agent instances
        # For now, we simulate agent responses
        agent_results = {}
        
        for agent_config in state.get("agent_configs", []):
            agent_name = agent_config["name"]
            logger.info(f"  → Delegating to {agent_name}")
            
            # Simulate agent work
            # For math agents, try to extract and solve simple arithmetic
            result_text = f"Agent {agent_name} completed its assigned task"
            
            if agent_config.get("type") == "calculator" or "math" in agent_config.get("capabilities", []):
                # Try to extract simple math from the task
                import re
                task = state["task"]
                # Look for simple arithmetic patterns like "6 + 999"
                math_match = re.search(r'(\d+)\s*\+\s*(\d+)', task)
                if math_match:
                    num1, num2 = int(math_match.group(1)), int(math_match.group(2))
                    answer = num1 + num2
                    result_text = f"Calculated: {num1} + {num2} = {answer}"
            
            agent_results[agent_name] = {
                "status": "completed",
                "result": result_text,
                "timestamp": datetime.utcnow().isoformat()
            }
        
        return {
            "agent_results": agent_results,
            "current_step": "delegated"
        }
    
    async def _aggregate_results(self, state: OrchestratorState) -> dict:
        """Aggregate results from all agents."""
        logger.info("📊 Aggregating results")
        
        results_summary = "\n".join([
            f"- {name}: {result['result']}"
            for name, result in state["agent_results"].items()
        ])
        
        messages = state["messages"] + [
            HumanMessage(content=f"""Aggregate these agent results:

{results_summary}

Synthesize them into a coherent summary.""")
        ]
        
        response = await self.llm.ainvoke(messages)
        
        return {
            "messages": state["messages"] + [response],
            "current_step": "aggregated"
        }
    
    async def _finalize_output(self, state: OrchestratorState) -> dict:
        """Finalize the output."""
        logger.info("✅ Finalizing output")
        
        final_message = state["messages"][-1]
        final_output = final_message.content
        
        # Store final output in memory
        self.memory.save_interaction(
            session_id=state.get("session_id", "default"),
            role="orchestrator",
            content=f"Final output: {final_output}",
            metadata={
                "task": state["task"],
                "timestamp": datetime.utcnow().isoformat(),
                "agent_count": len(state.get("agent_configs", []))
            }
        )
        
        return {
            "final_output": final_output,
            "current_step": "finalized"
        }
    
    async def run(
        self,
        task: str,
        agent_configs: list[dict],
        session_id: str = None
    ) -> dict:
        """Run the orchestrator workflow.
        
        Args:
            task: The task to execute
            agent_configs: List of agent configurations
            session_id: Optional session ID for memory persistence
            
        Returns:
            Dictionary with final output and metadata
        """
        logger.info(f"🎯 Starting orchestrator for task: {task}")
        
        initial_state = {
            "messages": [HumanMessage(content=task)],
            "task": task,
            "plan": "",
            "agent_configs": agent_configs,
            "agent_results": {},
            "final_output": "",
            "current_step": "initialized",
            "session_id": session_id or f"session_{datetime.utcnow().timestamp()}"
        }
        
        # Execute the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        return {
            "output": final_state.get("final_output", ""),
            "plan": final_state.get("plan", ""),
            "agent_results": final_state.get("agent_results", {}),
            "session_id": final_state.get("session_id", session_id or f"session_{datetime.utcnow().timestamp()}")
        }


if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example usage
        orchestrator = OrchestratorAgent()
        
        result = await orchestrator.run(
            task="Analyze Q4 sales data and create an executive summary",
            agent_configs=[
                {"name": "data_analyst", "mcp_servers": ["http://localhost:9000/mcp"]},
                {"name": "report_writer", "mcp_servers": ["http://localhost:9000/mcp"]}
            ]
        )
        
        print(f"\n✅ Final Output:\n{result['output']}")
        print(f"\n📋 Session ID: {result['session_id']}")
    
    asyncio.run(main())

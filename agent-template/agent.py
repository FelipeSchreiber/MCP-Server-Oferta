"""MCP Agent with LangChain integration."""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import httpx
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field

from config import settings
from memory import MongoMemory
from mcp_client import MCPClient

logger = logging.getLogger(__name__)


class MCPAgent:
    """Agent that integrates with MCP servers and uses MongoDB for memory."""
    
    def __init__(
        self,
        name: str,
        mcp_servers: List[str],
        mongo_uri: str = None,
        model: str = "gpt-4-turbo-preview"
    ):
        """Initialize the MCP agent.
        
        Args:
            name: Agent name
            mcp_servers: List of MCP server URLs
            mongo_uri: MongoDB connection URI
            model: LLM model to use
        """
        self.name = name
        self.mcp_servers = mcp_servers
        self.mongo_uri = mongo_uri or settings.mongodb_uri
        self.memory = MongoMemory(self.mongo_uri)
        self.llm = ChatOpenAI(model=model, temperature=0)
        
        # Initialize MCP clients and tools
        self.mcp_clients = [MCPClient(url) for url in mcp_servers]
        self.tools = []
        self._load_tools()
        
        # Create system prompt
        self.system_prompt = self._create_system_prompt()
        
        logger.info(f"✅ Agent '{name}' initialized with {len(self.tools)} tools")
    
    def _load_tools(self):
        """Load tools from all MCP servers."""
        logger.info(f"🔧 Loading tools from {len(self.mcp_servers)} MCP servers...")
        
        for client in self.mcp_clients:
            try:
                # Get available tools from MCP server
                tools_list = client.list_tools()
                
                for tool_info in tools_list:
                    # Create tool dictionary
                    tool = {
                        "name": tool_info["name"],
                        "description": tool_info.get("description", ""),
                        "client": client
                    }
                    self.tools.append(tool)
                    logger.info(f"  ✓ Loaded tool: {tool_info['name']}")
                    
            except Exception as e:
                logger.error(f"  ✗ Failed to load tools from {client.url}: {e}")
    
    def _execute_mcp_tool(
        self,
        client: MCPClient,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> str:
        """Execute an MCP tool.
        
        Args:
            client: MCP client instance
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Tool result as string
        """
        try:
            result = client.call_tool(tool_name, arguments)
            return str(result.get("result", "No result"))
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return f"Error: {str(e)}"
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with available tools."""
        return f"""You are {self.name}, an AI agent designed to help with specific tasks.

You have access to the following tools from MCP servers:
{self._format_tools_description()}

When you need to use a tool, respond with:
TOOL_CALL: tool_name
ARGS: {{"arg1": "value1", "arg2": "value2"}}

After getting tool results, provide a final answer."""
    
    def _format_tools_description(self) -> str:
        """Format tools for prompt."""
        return "\n".join([
            f"- {tool['name']}: {tool['description']}"
            for tool in self.tools
        ])
    
    def _find_tool(self, tool_name: str):
        """Find tool by name."""
        for tool in self.tools:
            if tool["name"] == tool_name:
                return tool
        return None
    
    async def run(
        self,
        task: str,
        session_id: str = None,
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """Run the agent on a task.
        
        Args:
            task: Task description
            session_id: Optional session ID for memory
            max_iterations: Maximum iterations
            
        Returns:
            Dictionary with output and metadata
        """
        logger.info(f"🎯 Agent '{self.name}' starting task: {task}")
        
        session_id = session_id or f"session_{datetime.utcnow().timestamp()}"
        
        # Get chat history from memory
        history = self.memory.get_session_history(session_id, limit=10)
        chat_history = []
        for msg in history:
            if msg["role"] == "user":
                chat_history.append(f"User: {msg['content']}")
            elif msg["role"] == "assistant":
                chat_history.append(f"Assistant: {msg['content']}")
        
        # Save user message
        self.memory.save_interaction(
            session_id=session_id,
            role="user",
            content=task,
            metadata={"agent": self.name}
        )
        
        # Build conversation
        messages = [SystemMessage(content=self.system_prompt)]
        if chat_history:
            context = "\n".join(chat_history)
            messages.append(HumanMessage(content=f"Previous context:\n{context}"))
        messages.append(HumanMessage(content=f"Task: {task}"))
        
        try:
            # Get LLM response
            response = self.llm.invoke(messages)
            output = response.content
            
            # Check if LLM wants to use a tool
            if "TOOL_CALL:" in output:
                lines = output.split("\n")
                tool_name = None
                args_str = None
                
                for i, line in enumerate(lines):
                    if line.startswith("TOOL_CALL:"):
                        tool_name = line.replace("TOOL_CALL:", "").strip()
                    elif line.startswith("ARGS:"):
                        args_str = line.replace("ARGS:", "").strip()
                
                if tool_name and args_str:
                    try:
                        args = eval(args_str)  # Simple parsing
                        tool = self._find_tool(tool_name)
                        
                        if tool:
                            # Execute tool
                            result = self._execute_mcp_tool(
                                tool["client"],
                                tool_name,
                                args
                            )
                            
                            # Get final response with tool result
                            messages.append(AIMessage(content=output))
                            messages.append(HumanMessage(content=f"Tool result: {result}"))
                            
                            final_response = self.llm.invoke(messages)
                            output = final_response.content
                    except Exception as e:
                        logger.error(f"Error executing tool: {e}")
                        output = f"Tool execution failed: {str(e)}"
            
            # Save assistant response
            self.memory.save_interaction(
                session_id=session_id,
                role="assistant",
                content=output,
                metadata={
                    "agent": self.name,
                    "tools_available": len(self.tools)
                }
            )
            
            logger.info(f"✅ Agent '{self.name}' completed task")
            
            return {
                "output": output,
                "session_id": session_id,
                "agent": self.name,
                "tools_available": len(self.tools)
            }
            
        except Exception as e:
            logger.error(f"❌ Agent error: {e}")
            return {
                "output": f"Error: {str(e)}",
                "session_id": session_id,
                "agent": self.name,
                "error": True
            }


if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example usage
        agent = MCPAgent(
            name="demo_agent",
            mcp_servers=["http://localhost:9000/mcp"]
        )
        
        result = await agent.run(
            task="Add the numbers 15 and 27",
            session_id="demo_session"
        )
        
        print(f"\n✅ Result:\n{result['output']}")
    
    asyncio.run(main())

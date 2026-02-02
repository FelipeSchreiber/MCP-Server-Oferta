"""MCP Client for communicating with MCP servers."""

import logging
from typing import List, Dict, Any, Optional

import httpx

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for MCP server communication."""
    
    def __init__(self, url: str, timeout: int = 30):
        """Initialize MCP client.
        
        Args:
            url: MCP server URL
            timeout: Request timeout in seconds
        """
        self.url = url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout)
        logger.info(f"📡 MCP Client initialized for {self.url}")
    
    def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send JSON-RPC request to MCP server.
        
        Args:
            method: RPC method name
            params: Method parameters
            
        Returns:
            Response dictionary
        """
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        try:
            response = self.client.post(
                self.url,
                json=request_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise Exception(f"MCP Error: {data['error']}")
            
            return data.get("result", {})
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error communicating with MCP server: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending MCP request: {e}")
            raise
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from MCP server.
        
        Returns:
            List of tool descriptions
        """
        logger.info(f"📋 Listing tools from {self.url}")
        
        try:
            result = self._send_request("tools/list")
            tools = result.get("tools", [])
            
            logger.info(f"✅ Found {len(tools)} tools")
            return tools
            
        except Exception as e:
            logger.error(f"Failed to list tools: {e}")
            return []
    
    def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        logger.info(f"🔧 Calling tool '{tool_name}' with args: {arguments}")
        
        params = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        
        try:
            result = self._send_request("tools/call", params)
            logger.info(f"✅ Tool '{tool_name}' executed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to call tool '{tool_name}': {e}")
            raise
    
    def get_prompts(self) -> List[Dict[str, Any]]:
        """Get available prompts from MCP server.
        
        Returns:
            List of prompt descriptions
        """
        logger.info(f"📝 Getting prompts from {self.url}")
        
        try:
            result = self._send_request("prompts/list")
            prompts = result.get("prompts", [])
            
            logger.info(f"✅ Found {len(prompts)} prompts")
            return prompts
            
        except Exception as e:
            logger.error(f"Failed to get prompts: {e}")
            return []
    
    def get_resources(self) -> List[Dict[str, Any]]:
        """Get available resources from MCP server.
        
        Returns:
            List of resource descriptions
        """
        logger.info(f"📦 Getting resources from {self.url}")
        
        try:
            result = self._send_request("resources/list")
            resources = result.get("resources", [])
            
            logger.info(f"✅ Found {len(resources)} resources")
            return resources
            
        except Exception as e:
            logger.error(f"Failed to get resources: {e}")
            return []
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
        logger.info(f"🔌 MCP Client closed for {self.url}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    # Example usage
    with MCPClient("http://localhost:9000/mcp") as client:
        # List tools
        tools = client.list_tools()
        print(f"\n📋 Available tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool['name']}: {tool.get('description', 'N/A')}")
        
        # Call a tool
        if tools:
            result = client.call_tool("add_two_numbers", {"a": 5, "b": 3})
            print(f"\n✅ Tool result: {result}")

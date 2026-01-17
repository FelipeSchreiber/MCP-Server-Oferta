from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
import re
from typing import Dict, Any, List

load_dotenv()

# Configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000/mcp")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

client = OpenAI(api_key=OPENAI_API_KEY)

# Store the MCP session ID
mcp_session_id = None


def parse_sse_response(response_text: str) -> dict:
    """Parse Server-Sent Events format response."""
    lines = response_text.strip().split('\n')
    for line in lines:
        if line.startswith('data: '):
            return json.loads(line[6:])  # Remove 'data: ' prefix
    return {}


def initialize_mcp_session():
    """Initialize the MCP session with the server."""
    global mcp_session_id
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "FastMCPClient", "version": "1.0"}
                }
            },
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=5
        )
        response.raise_for_status()
        
        # Extract session ID from response headers
        mcp_session_id = response.headers.get("mcp-session-id")
        
        parse_sse_response(response.text)
        print(f"✅ MCP session initialized (ID: {mcp_session_id})")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize MCP session: {e}")
        return False


def retrieve_mcp_tools(server_url: str = MCP_SERVER_URL) -> List[Dict[str, Any]]:
    """Retrieve available tools from the FastMCP server."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if mcp_session_id:
            headers["mcp-session-id"] = mcp_session_id
        
        response = requests.post(
            server_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list",
                "params": {}
            },
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        
        tools_data = parse_sse_response(response.text)
        
        openai_tools = []
        if "result" in tools_data and "tools" in tools_data["result"]:
            for tool in tools_data["result"]["tools"]:
                openai_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.get("name", "unknown"),
                        "description": tool.get("description", ""),
                        "parameters": tool.get("inputSchema", {
                            "type": "object",
                            "properties": {},
                            "required": []
                        })
                    }
                })
        return openai_tools
    except Exception as e:
        print(f"Warning: Could not retrieve tools: {e}")
        return []


def retrieve_mcp_resources(server_url: str = MCP_SERVER_URL) -> List[Dict[str, Any]]:
    """Retrieve available resources from the FastMCP server and convert them to tools."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if mcp_session_id:
            headers["mcp-session-id"] = mcp_session_id
        
        response = requests.post(
            server_url,
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/list",
                "params": {}
            },
            headers=headers,
            timeout=5
        )
        response.raise_for_status()
        
        resources_data = parse_sse_response(response.text)
        
        resource_tools = []
        if "result" in resources_data and "resources" in resources_data["result"]:
            for resource in resources_data["result"]["resources"]:
                uri_template = resource.get("uri", "")
                name = resource.get("name", "unknown_resource")
                description = resource.get("description", "")
                
                # Extract parameters from URI template
                params = re.findall(r'\{(\w+)\}', uri_template)
                
                properties = {}
                for param in params:
                    properties[param] = {
                        "type": "integer" if "id" in param else "string",
                        "description": f"The {param} parameter"
                    }
                
                resource_tools.append({
                    "type": "function",
                    "function": {
                        "name": f"resource_{name}",
                        "description": f"Read resource: {description}",
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": list(properties.keys())
                        }
                    }
                })
        
        return resource_tools
    except Exception as e:
        print(f"Warning: Could not retrieve resources: {e}")
        return []


def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Call a tool on the MCP server."""
    try:
        # Check if this is a resource call
        if tool_name.startswith("resource_"):
            return call_mcp_resource(tool_name, arguments)
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if mcp_session_id:
            headers["mcp-session-id"] = mcp_session_id
        
        response = requests.post(
            MCP_SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        result = parse_sse_response(response.text)
        
        if "result" in result:
            if isinstance(result["result"], dict) and "content" in result["result"]:
                content = result["result"]["content"]
                if content and isinstance(content, list) and len(content) > 0:
                    return str(content[0].get("text", content[0]))
            return json.dumps(result["result"])
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


def call_mcp_resource(resource_name: str, arguments: Dict[str, Any]) -> str:
    """Read a resource from the MCP server."""
    try:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        if mcp_session_id:
            headers["mcp-session-id"] = mcp_session_id
        
        # Remove "resource_" prefix
        actual_name = resource_name.replace("resource_", "")
        
        # Build the URI from arguments
        if actual_name == "get_user_profile" and "user_id" in arguments:
            uri = f"users://{arguments['user_id']}/profile"
        elif actual_name == "get_config":
            uri = "config://app_config"
        else:
            uri = actual_name
        
        response = requests.post(
            MCP_SERVER_URL,
            json={
                "jsonrpc": "2.0",
                "id": 4,
                "method": "resources/read",
                "params": {
                    "uri": uri
                }
            },
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        
        result = parse_sse_response(response.text)
        
        # Extract resource content
        if "result" in result and "contents" in result["result"]:
            contents = result["result"]["contents"]
            if contents and len(contents) > 0:
                content_item = contents[0]
                if "text" in content_item:
                    return content_item["text"]
                return json.dumps(content_item)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


# Main execution
print(f"Retrieving tools and resources from {MCP_SERVER_URL}...")
initialize_mcp_session()
tools = retrieve_mcp_tools()
resources = retrieve_mcp_resources()
all_tools = tools + resources
print(f"Retrieved {len(tools)} tool(s) and {len(resources)} resource(s)")

# Create messages
messages = [
    {"role": "system", "content": "You are a helpful assistant with access to MCP server tools and resources."},
    {"role": "user", "content": "retrieve user profile for user_id 42 and add two numbers: 15 and 27"}
]

# Function calling loop
max_iterations = 5
for iteration in range(max_iterations):
    print(f"\nIteration {iteration + 1}")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=all_tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
        messages.append(message)
        
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"Calling: {function_name}({function_args})")
            result = call_mcp_tool(function_name, function_args)
            print(f"Result: {result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": result
            })
    else:
        print(f"\nFinal Response: {message.content}")
        break

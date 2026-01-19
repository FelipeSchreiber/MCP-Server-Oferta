"""
Simple MCP Client - Minimal code to interact with MCP server
"""
import json
import requests

# Load MCP server config
with open('.vscode/mcp.json', 'r') as f:
    config = json.load(f)

SERVER_URL = config['servers']['DemoServer']['url']
session_id = None


def init_session():
    """Initialize MCP session"""
    global session_id
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0", "id": 0, "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, 
                   "clientInfo": {"name": "simple-client", "version": "1.0"}}
    }, headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    session_id = r.headers.get('mcp-session-id')
    return session_id


def call_tool(tool_name: str, args: dict) -> dict:
    """Call an MCP tool"""
    r = requests.post(SERVER_URL, json={
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {"name": tool_name, "arguments": args}
    }, headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream", 
                "mcp-session-id": session_id})
    
    # Parse SSE response
    for line in r.text.split('\n'):
        if line.startswith('data: '):
            data = json.loads(line[6:])
            if 'result' in data:
                return data['result']
    return {}


# Main
if __name__ == "__main__":
    print(f"Connecting to: {SERVER_URL}")
    init_session()
    print(f"Session ID: {session_id}\n")
    
    # Example: Add two numbers
    result = call_tool("add_two_numbers", {"a": 15, "b": 27})
    print(f"15 + 27 = {result['content'][0]['text']}")
    
    # Example: Get user info (requires approval)
    result = call_tool("get_user_info", {"user_id": 42})
    print(f"\nUser 42 info: {result}")
